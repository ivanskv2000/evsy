from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from app.modules.auth.schemas import OAuthLogin
from app.settings import Settings

settings = Settings()

# GitHub config
GITHUB_CLIENT_ID = settings.github_client_id
GITHUB_CLIENT_SECRET = settings.github_client_secret

GITHUB_USER_API = "https://api.github.com/user"
GITHUB_EMAILS_API = "https://api.github.com/user/emails"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_SCOPE = "user:email"

# Google config
GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret
GOOGLE_USERINFO_API = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_SCOPE = "openid email profile"


def get_email_from_github(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        with httpx.Client() as client:
            email_resp = client.get(GITHUB_EMAILS_API, headers=headers, timeout=5.0)
            print("[GITHUB EMAIL LOOKUP] status:", email_resp.status_code)
            print("[GITHUB EMAIL LOOKUP] response:", email_resp.text)

    except httpx.ReadTimeout as err:
        raise HTTPException(status_code=504, detail="GitHub API timed out") from err

    if email_resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch GitHub email")

    emails = email_resp.json()
    primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
    if not primary:
        raise HTTPException(status_code=400, detail="No verified primary GitHub email")
    return primary["email"]


def get_email_from_google(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        with httpx.Client() as client:
            resp = client.get(GOOGLE_USERINFO_API, headers=headers, timeout=5.0)
    except httpx.ReadTimeout as err:
        raise HTTPException(status_code=504, detail="Google API timed out") from err

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch Google user info")

    data = resp.json()
    email = data.get("email")
    verified = data.get("email_verified")
    if not email or not verified:
        raise HTTPException(status_code=400, detail="Email not verified by Google")
    return email


def get_email_from_oauth(login: OAuthLogin) -> str:
    # redirect_uri = f"{settings.api_url}/auth/oauth/callback?provider={login.provider}"
    redirect_uri = (
        f"http://localhost:8000/api/v1/auth/oauth/callback?provider={login.provider}"
    )

    return exchange_code_for_email(login.provider, login.token, redirect_uri)


def build_oauth_redirect(provider: str, redirect_uri: str, state: str) -> str:
    if provider == "github":
        query = urlencode(
            {
                "client_id": GITHUB_CLIENT_ID,
                "redirect_uri": redirect_uri,
                "scope": GITHUB_SCOPE,
                "state": state,
                "response_type": "code",
            }
        )
        return f"{GITHUB_AUTH_URL}?{query}"

    elif provider == "google":
        query = urlencode(
            {
                "client_id": GOOGLE_CLIENT_ID,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": GOOGLE_SCOPE,
                "state": state,
                "access_type": "offline",
                "prompt": "consent",
            }
        )
        return f"{GOOGLE_AUTH_URL}?{query}"

    raise HTTPException(status_code=400, detail="Unsupported provider")


def exchange_code_for_email(provider: str, code: str, redirect_uri: str) -> str:
    if provider == "github":
        try:
            token_resp = httpx.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
                timeout=5.0,
            )
            print("[GITHUB TOKEN EXCHANGE] status:", token_resp.status_code)
            print("[GITHUB TOKEN EXCHANGE] response:", token_resp.text)

            token_resp.raise_for_status()
            access_token = token_resp.json().get("access_token")
            if not access_token:
                raise HTTPException(
                    status_code=400, detail="GitHub did not return access token"
                )
            return get_email_from_github(access_token)

        except Exception as e:
            import traceback

            print("[GITHUB OAUTH ERROR]", traceback.format_exc())
            raise HTTPException(status_code=400, detail="GitHub token exchange failed") from e

    elif provider == "google":
        token_resp = httpx.post(
            "https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=5.0,
        )
        token_resp.raise_for_status()
        access_token = token_resp.json().get("access_token")
        return get_email_from_google(access_token)

    raise HTTPException(status_code=400, detail="Unsupported provider")

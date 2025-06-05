from urllib.parse import urlencode

import httpx
from fastapi import HTTPException

from app.modules.auth.schemas import OAuthLogin
from app.settings import Settings

settings = Settings()

# --- Provider-specific logic ---


def get_email_from_github(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = httpx.get(
            "https://api.github.com/user/emails", headers=headers, timeout=5.0
        )
    except httpx.ReadTimeout as err:
        raise HTTPException(status_code=504, detail="GitHub API timed out") from err

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch GitHub email")

    emails = resp.json()
    primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
    if not primary:
        raise HTTPException(status_code=400, detail="No verified primary GitHub email")
    return primary["email"]


def get_email_from_google(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = httpx.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers=headers,
            timeout=5.0,
        )
    except httpx.ReadTimeout as err:
        raise HTTPException(status_code=504, detail="Google API timed out") from err

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch Google user info")

    data = resp.json()
    if not data.get("email") or not data.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email not verified by Google")
    return data["email"]


# --- Provider config registry ---

OAUTH_PROVIDERS = {
    "github": {
        "client_id": settings.github_client_id,
        "client_secret": settings.github_client_secret,
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "scope": "user:email",
        "email_fetcher": get_email_from_github,
        "headers": {"Accept": "application/json"},
    },
    "google": {
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "scope": "openid email profile",
        "email_fetcher": get_email_from_google,
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "extra_auth_params": {"access_type": "offline", "prompt": "consent"},
    },
}

# --- Generic Logic ---


def build_oauth_redirect(provider: str, redirect_uri: str, state: str) -> str:
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    cfg = OAUTH_PROVIDERS[provider]
    query = {
        "client_id": cfg["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": cfg["scope"],
        "state": state,
    }
    query.update(cfg.get("extra_auth_params", {}))

    return f"{cfg['auth_url']}?{urlencode(query)}"


def _post_token_request(url: str, data: dict, headers: dict) -> dict:
    resp = httpx.post(url, headers=headers, data=data, timeout=5.0)
    resp.raise_for_status()
    return resp.json()


def exchange_code_for_email(provider: str, code: str, redirect_uri: str) -> str:
    if provider not in OAUTH_PROVIDERS:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    cfg = OAUTH_PROVIDERS[provider]
    try:
        data = {
            "code": code,
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }
        token_resp = _post_token_request(cfg["token_url"], data, cfg["headers"])
        access_token = token_resp.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail=f"{provider.title()} did not return access token",
            )

        return cfg["email_fetcher"](access_token)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"{provider.title()} token exchange failed"
        ) from e


def get_email_from_oauth(login: OAuthLogin) -> str:
    redirect_uri = "http://localhost:8000/api/v1/auth/oauth/callback"
    return exchange_code_for_email(login.provider, login.token, redirect_uri)

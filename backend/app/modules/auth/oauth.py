import httpx
from fastapi import HTTPException

from app.modules.auth.schemas import OAuthLogin

# GitHub config
GITHUB_CLIENT_ID = "your_github_client_id"
GITHUB_CLIENT_SECRET = "your_github_client_secret"
GITHUB_USER_API = "https://api.github.com/user"
GITHUB_EMAILS_API = "https://api.github.com/user/emails"

# Google config
GOOGLE_USERINFO_API = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_email_from_github(token: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    try:
        with httpx.Client() as client:
            email_resp = client.get(GITHUB_EMAILS_API, headers=headers, timeout=5.0)
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="GitHub API timed out")

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
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Google API timed out")

    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch Google user info")
    data = resp.json()
    email = data.get("email")
    verified = data.get("email_verified")
    if not email or not verified:
        raise HTTPException(status_code=400, detail="Email not verified by Google")
    return email


def get_email_from_oauth(login: OAuthLogin) -> str:
    if login.provider == "github":
        return get_email_from_github(login.token)
    elif login.provider == "google":
        return get_email_from_google(login.token)
    raise HTTPException(status_code=400, detail="Unsupported provider")

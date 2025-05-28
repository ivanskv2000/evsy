import base64
import json

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth import crud, oauth, schemas, service
from app.modules.auth.models import User
from app.modules.auth.schemas import (
    OAuthLogin,
    ProviderName,
    TokenOut,
    UserCreate,
    UserLogin,
)
from app.modules.auth.token import create_access_token, get_current_user
from app.settings import Settings

settings = Settings()

router = APIRouter()


@router.post("/signup", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    user = service.create_user(db, user_in)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenOut)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, user_in.email)
    if (
        not user
        or not user.hashed_password
        or not service.verify_password(user_in.password, user.hashed_password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/oauth", response_model=TokenOut)
def login_oauth(payload: OAuthLogin, db: Session = Depends(get_db)):
    email = oauth.get_email_from_oauth(payload)
    user = service.get_or_create_oauth_user(db, email=email, provider=payload.provider)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/oauth/init/{provider}")
def start_oauth_login(
    provider: ProviderName,
    request: Request,
    redirect: str = Query("/events"),
):
    redirect_uri = request.url_for("oauth_callback")

    state_payload = {
        "provider": provider,
        "redirect": redirect,
    }
    state = base64.urlsafe_b64encode(json.dumps(state_payload).encode()).decode()

    url = oauth.build_oauth_redirect(provider, redirect_uri, state)
    return RedirectResponse(url=url)


@router.get("/oauth/callback", name="oauth_callback")
def handle_oauth_callback(
    code: str = Query(...),
    state: str = Query(...),
):
    final_url = f"{settings.frontend_url}/oauth/callback?code={code}&state={state}"
    return RedirectResponse(url=final_url)

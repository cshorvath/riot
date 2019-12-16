from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import api.model.user as api_model
import api.repository.user as user_repository
import core.model as db_model
from api.bootstrap import get_db, SECRET_KEY
from api.model.auth import Token
from api.util.auth import verify_password


def get_authenticated_user(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user: db_model.User = user_repository.get_user_by_name(db, form_data.username)
    if user and verify_password(form_data.password, user.password):
        return api_model.User(**user.__dict__)
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


router = APIRouter()


@router.post("", response_model=Token)
async def login_for_access_token(
        user: api_model.User = Depends(get_authenticated_user)
):
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=24 * 60)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

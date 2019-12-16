import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

import api.repository.user as user_repository
from api.bootstrap import get_db, SECRET_KEY, ALGORITHM
from api.repository.device import user_owns_device
from core.model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (PyJWTError, ValidationError, TypeError, ValueError):
        raise credentials_exception
    user = user_repository.get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user


def admin_user(user: User = Depends(get_current_user)):
    if not user.admin:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Admin required"
        )


def owner_user(
        device_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if not (user.admin or user_owns_device(db, user.id, device_id)):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Device not found."
        )
    return user

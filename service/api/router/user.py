from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.status import HTTP_409_CONFLICT, HTTP_404_NOT_FOUND

import api.repository.user as user_repository
from api.bootstrap import get_db
from api.model.user import NewUser, User

router = APIRouter()


@router.get("/", response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    return user_repository.get_all_users(db)


@router.post("/", response_model=User)
def create_user(user: NewUser, db: Session = Depends(get_db)):
    try:
        return user_repository.create_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="DUPLICATED_USER"
        )


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_repository.delete_user(db, user_id)
    if not result:
        raise HTTPException(HTTP_404_NOT_FOUND)

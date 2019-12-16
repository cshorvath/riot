from fastapi import APIRouter, Depends

from api.model.user import User
from api.util.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=User)
def get_current_user(user: User = Depends(get_current_user)):
    return user

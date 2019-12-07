from sqlalchemy.orm import Session

from api.auth import get_password_hash
from api.model.user import NewUser
from core import model


def get_all_users(db: Session):
    return db.query(model.User).all()


def get_user(db: Session, user_id: int) -> model.User:
    return db.query(model.User).get(user_id)


def get_user_by_name(db: Session, user_name: str) -> model.User:
    return db.query(model.User).filter_by(name=user_name)


def create_user(db: Session, user: NewUser) -> model.User:
    inserted_user = model.User(name=user.name, password=get_password_hash(user.password), admin=False)
    db.add(inserted_user)
    db.commit()
    db.refresh(inserted_user)
    return inserted_user


def delete_user(db: Session, user_id: int) -> bool:
    delete_count = db.query(model.User).filter_by(id=user_id).delete()
    db.commit()
    return delete_count

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.bootstrap import get_db
from api.model.rule import NewRule, RuleResponse
from api.router.user import get_current_user
from core.model import User

router = APIRouter()


@router.get("{device_id}/rule", response_model=List[RuleResponse])
def get_rules_for_device(
        device_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    pass


@router.post("{device_id}/rule")
def add_rule_for_device(
        device_id: int,
        rule: NewRule,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    pass


@router.patch("{device_id}/rule/{rule_id}", response_model=RuleResponse)
def update_rule(
        device_id: int,
        rule_id: int,
        rule: NewRule,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    pass


@router.delete("{device_id}/rule/{rule_id}")
def delete_rule(
        device_id: int,
        rule_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    pass

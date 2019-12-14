from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

import api.repository.rule as rule_repository
from api.bootstrap import get_db
from api.model.rule import RuleRequest, RuleResponse
from api.util.auth import owner_user, get_current_user
from api.util.validation import validate_rule
from core.model import User

router = APIRouter()


@router.get("/device/{device_id}/rule", dependencies=[Depends(owner_user)], response_model=List[RuleResponse])
def get_rules_for_device(
        device_id: int,
        db: Session = Depends(get_db)
):
    return rule_repository.get_rules_for_device(db, device_id)


@router.get("/rule", response_model=List[RuleResponse])
def get_rules_for_user(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return rule_repository.get_rules_for_user(db, user)


@router.post("/device/{device_id}/rule")
def add_rule_for_device(
        device_id: int,
        rule: RuleRequest,
        user: User = Depends(owner_user),
        db: Session = Depends(get_db)
):
    validate_rule(rule)
    return rule_repository.insert_rule(db, device_id, rule, user)


@router.put("/device/{device_id}/rule/{rule_id}", dependencies=[Depends(owner_user)], response_model=RuleResponse)
def update_rule(
        rule_id: int,
        rule: RuleRequest,
        db: Session = Depends(get_db)
):
    validate_rule(rule)
    rule = rule_repository.update_rule(db, rule_id, rule)
    if not rule:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Rule not found."
        )
    return rule


@router.delete("/device/{device_id}/rule/{rule_id}", dependencies=[Depends(owner_user)])
def delete_rule(
        rule_id: int,
        db: Session = Depends(get_db)
):
    if not rule_repository.delete_rule(db, rule_id):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Rule not found."
        )

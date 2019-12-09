from sqlalchemy.orm import Session

from api.model.rule import NewRule, PatchRule
from core.model import Rule, Device, User


def get_rules_for_device(db: Session, device_id: int):
    return db.query(Rule).filter_by(source_device_id=device_id).all()


def get_rules_for_user(db: Session, user: User):
    if user.admin:
        return db.query(Rule).all()
    return db.query(Rule).join(Rule.source_device).join(Device.owners).filter(User.id == user.id).all()


def insert_rule(db: Session, device_id: int, rule: NewRule, user: User) -> Rule:
    db_rule = Rule(creator_id=user.id, source_device_id=device_id, **rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


def delete_rule(db: Session, rule_id: int) -> bool:
    result = db.query(Rule).filter_by(id=rule_id).delete()
    db.commit()
    return bool(result)


def patch_rule(db: Session, rule_id: int, rule: PatchRule):
    result = db.query(Rule).filter_by(id=rule_id).update(rule.dict(exclude_unset=True))
    db.commit()
    if result:
        return db.query(Rule).get(rule_id)
    return None

import enum

from sqlalchemy import Column, Enum, Integer, String, Table, Boolean, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.orm import relationship

from common.model import Base

user_device = Table(
    "user_device",
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('device_id', Integer, ForeignKey('device.id'), nullable=False)
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True)
    password = Column(String(40))
    admin = Column(Boolean, default=False, nullable=False)

    devices = relationship("Device", secondary=user_device)


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True, index=True, nullable=False)
    display_name = Column(String(40), nullable=True)
    description = Column(String(255))

    owners = relationship("User", secondary=user_device)
    messages = relationship("Message", back_populates="device")
  #  rules = relationship("Rule", back_populates="source_device", foreign_keys="rule.source_device_id")


class MessageDirection(enum.Enum):
    INBOUND = 1
    OUTBOUND = 2


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, index=True)
    device_id = Column(Integer, ForeignKey("device.id"), index=True, nullable=False)
    direction = Column(Enum(MessageDirection), nullable=False)
    payload = Column(JSON, nullable=True)  # TODO

    device = relationship("Device", back_populates="messages")


class RuleOperatorId(enum.Enum):
    LT = 1
    LTE = 2
    GT = 3
    GTE = 4
    EQ = 5
    BETWEEN = 6


class RuleAction(enum.Enum):
    SEND_EMAIL = 1
    FORWARD = 2


"""
class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    source_device_id = Column(Integer, ForeignKey("device.id"), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    field_selector = Column(Text, nullable=False)
    operator = Column(Enum(RuleOperatorId), nullable=False)
    operator_arg_1 = Column(Numeric, nullable=False)
    operator_arg_2 = Column(Numeric)
    action = Column(Enum(RuleAction), nullable=False)
    action_arg = Column(Text, nullable=False)
    target_device_id = Column(Integer, ForeignKey("device.id"))

    source_device = relationship("Device", foreign_keys=[source_device_id], back_populates="rules")
    target_device = relationship("Device", foreign_keys=[target_device_id])
    creator = relationship("User")
"""

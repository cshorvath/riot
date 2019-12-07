import enum

from sqlalchemy import Column, Enum, Integer, String, Boolean, ForeignKey, TIMESTAMP, JSON, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserDevice(Base):
    __tablename__ = "user_device"

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False, primary_key=True, )
    device_id = Column(Integer, ForeignKey('device.id', ondelete="CASCADE"), nullable=False, primary_key=True)

    user = relationship("User", back_populates="devices")
    device = relationship("Device", back_populates="owners")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), unique=True)
    password = Column(String(255))
    admin = Column(Boolean, default=False, nullable=False)

    devices = relationship(UserDevice, back_populates="user")
    rules = relationship("Rule", back_populates="creator")


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), index=True, nullable=False)
    description = Column(String(255))

    owners = relationship(UserDevice, back_populates="device")
    messages = relationship("Message", back_populates="device")
    source_rules = relationship("Rule", back_populates="source_device", foreign_keys="Rule.source_device_id")
    target_rules = relationship("Rule", back_populates="target_device", foreign_keys="Rule.target_device_id")


class MessageDirection(enum.Enum):
    INBOUND = 1
    OUTBOUND = 2


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP, index=True)
    device_id = Column(Integer, ForeignKey("device.id"), index=True, nullable=False)
    direction = Column(Enum(MessageDirection), nullable=False)
    payload = Column(JSON, nullable=True)

    device = relationship("Device", back_populates="messages")


class RuleOperator(enum.Enum):
    LT = 1
    LTE = 2
    GT = 3
    GTE = 4
    EQ = 5
    NE = 6
    BETWEEN = 7
    ANY = 8


class ActionType(enum.Enum):
    SEND_EMAIL = 1
    FORWARD = 2


class Rule(Base):
    __tablename__ = "rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    source_device_id = Column(Integer, ForeignKey("device.id"), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    message_field = Column(Text, nullable=False)
    operator = Column(Enum(RuleOperator), nullable=False)
    operator_arg_1 = Column(Numeric, nullable=False)
    operator_arg_2 = Column(Numeric)
    action_type = Column(Enum(ActionType), nullable=False)
    action_arg = Column(Text, nullable=False)
    target_device_id = Column(Integer, ForeignKey("device.id"))

    source_device = relationship("Device", back_populates="source_rules", foreign_keys=source_device_id)
    target_device = relationship("Device", back_populates="target_rules", foreign_keys=target_device_id)
    creator = relationship("User", back_populates="rules")

from enum import Enum
from uuid import UUID, uuid4
from typing import List
from datetime import datetime as dt

from sqlalchemy.orm import relationship, Mapped, mapped_column, types
from sqlalchemy import String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DeliveryType(Enum):
    delayed = "delayed"
    instant = "instant"

class NotificationType(Enum):
    like = "like"
    news = "news" 

class NotificationStatus(Enum):
    not_sended = "not_sended"
    success = "success"
    failed = "failed"


class Notifications(Base):
    __tablename__ = "Notifications"
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        index=True,
        default_factory=uuid4
    )

    user_id: Mapped[UUID] = mapped_column(types.Uuid, nullable=False, unique=False)
    notification_dt: Mapped[dt] = mapped_column(DateTime)
    notify_at: Mapped[dt] = mapped_column(DateTime)
    delivery_type: Mapped[DeliveryType]
    type: Mapped[NotificationType]
    status: Mapped[NotificationStatus]

    template_id: Mapped[UUID] = mapped_column(ForeignKey("Templates.id"))
    template: Mapped["Templates"] = relationship(back_populates="notifications")



class AggregatedNotifications(Base):
    __tablename__ = "AggregatedNotifications"
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        index=True,
        default_factory=uuid4
    )

    user_id: Mapped[UUID] = mapped_column(types.Uuid, nullable=False, unique=False)
    notification_type: Mapped[NotificationType]
    notification_dt: Mapped[dt] = mapped_column(DateTime)


class TemplateVariableType(Enum):
    int = "int"
    str = "str"
    datetime = "datetime"


class TemplateVariables(Base):
    __tablename__ = "TemplateVariables"
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        index=True,
        default_factory=uuid4
    )
    
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    type: Mapped[TemplateVariableType]

    template_id: Mapped[UUID] = mapped_column(ForeignKey("Templates.id"))
    template: Mapped["Templates"] = relationship(back_populates="variables")


class Templates(Base):
    __tablename__ = "Templates"
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        index=True,
        default_factory=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    body: Mapped[str] = mapped_column(Text, nullable=False, uniqie=False)

    variables: Mapped[List["TemplateVariables"]] = relationship(
        back_populates="template", cascade='all, delete')

    notifications: Mapped[List["TemplateVariables"]] = relationship(
        back_populates="template", cascade='all, delete')


class UserNotificationSettings(Base):
    __tablename__ = "UserNotificationSettings"
    id: Mapped[UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        index=True,
        default_factory=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(types.Uuid, nullable=False, unique=False)
    notification_type: Mapped[NotificationType]
    allowed: Mapped[bool] = mapped_column(Boolean, default=True)
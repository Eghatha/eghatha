import datetime as dt
import enum
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.mutable import MutableList
import sqlalchemy.dialects.postgresql as pg
from geoalchemy2 import Geometry


class MessageType(enum.StrEnum):
    image = enum.auto()
    text = enum.auto()


class UserType(enum.StrEnum):
    user = enum.auto()
    admin = enum.auto()


PgUserType = pg.ENUM(UserType, name="user_type")
PgMessageType = pg.ENUM(MessageType, name="message_type")


class Base(DeclarativeBase):
    pass


class UserBase(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[UserType] = mapped_column(PgUserType)
    hashed_pwd: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )
    profession: Mapped[str] = mapped_column(String)
    skills: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(pg.ARRAY(item_type=String)), server_default="{}"
    )

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "auction",
    }


class User(UserBase):
    __tablename__ = None

    __mapper_args__ = {
        "polymorphic_identity": UserType.user,
    }


class Admin(UserBase):
    __tablename__ = None

    __mapper_args__ = {
        "polymorphic_identity": UserType.admin,
    }


class Event(Base):
    __tablename__ = "event"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    image_path: Mapped[str | None] = mapped_column(String)
    location = mapped_column(Geometry)
    criticality: Mapped[int] = mapped_column(Integer)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("event.id"))
    message_type: Mapped[MessageType] = mapped_column(PgMessageType)
    text: Mapped[str | None] = mapped_column(String)
    image_path: Mapped[str | None] = mapped_column(String)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("admin.id"))
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )


class Subscription(Base):
    __tablename__ = "subscription"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("event.id"), primary_key=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )


class Tags(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )

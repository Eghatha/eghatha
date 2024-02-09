import datetime as dt
from sqlalchemy import ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList
import sqlalchemy.dialects.postgresql as pg
from geoalchemy2 import Geometry
from db.enums import UserType, MessageType, PgUserType, PgMessageType




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

    events: Mapped["Event"] = relationship(back_populates="owner")

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

    owner = relationship(User, back_populates="events")
    tags: Mapped[list["Tags"]] = relationship("Tags", secondary="event_tag")

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

    owner: Mapped[User] = relationship()


class Subscription(Base):
    __tablename__ = "subscription"
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), primary_key=True
    )
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event.id"), primary_key=True
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )
    is_approved: Mapped[bool] = mapped_column(default=False)

    event: Mapped[Event] = relationship()


class Tags(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), index=True, server_default=func.now()
    )


class EventTag(Base):
    __tablename__ = "event_tag"
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("event.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tags.id"), primary_key=True
    )

    tag: Mapped[Tags] = relationship()
from pydantic import BaseModel, ConfigDict
import datetime as dt
from db.enums import MessageType


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    

class User(BaseSchema):
    id: int
    name: str
    hashed_pwd: str
    profession: str
    skills: list[str]
    created_at: dt.datetime
    events: list["Event"]


class Admin(User):
    ...


class Event(BaseSchema):
    id: int
    title: str
    image_path: str | None
    lat: float
    lon: float
    criticality: int
    created_by: int

    owner: User
    tags: list["Tags"]


class Messages(BaseSchema):
    id: int
    event_id: int
    message_type: MessageType
    text: str | None
    image_path: str | None
    created_by: int
    created_at: dt.datetime

    owner: User



class Subscription(BaseSchema):
    user_id: int
    event_id: int
    created_at: dt.datetime
    is_approved: bool

    event: Event

class Tags(BaseSchema):
    id: int
    text: str
    created_at: int

    event: Event
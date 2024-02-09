import enum
import sqlalchemy.dialects.postgresql as pg


class MessageType(enum.StrEnum):
    image = enum.auto()
    text = enum.auto()


class UserType(enum.StrEnum):
    user = enum.auto()
    admin = enum.auto()

    
PgUserType = pg.ENUM(UserType, name="user_type")
PgMessageType = pg.ENUM(MessageType, name="message_type")


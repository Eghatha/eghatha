import streamlit as st
from db.session import get_db
from db import models, schemas
import sqlalchemy as sa


def get_event(event_id: str) -> schemas.Event | None:
    event_id_int = int(event_id)
    db = get_db()
    query = sa.select(models.Event).where(models.Event.id == event_id_int)
    res = db.scalar(query)
    return schemas.Event.model_validate(res) if res else None


def get_event_owner(event_id: str) -> schemas.User | None:
    event_id_int = int(event_id)
    db = get_db()
    query = (
        sa.select(models.User).join(models.Event).where(models.Event.id == event_id_int)
    )
    res = db.scalar(query)
    return schemas.User.model_validate(res) if res else None


def get_event_tags(event_id: str) -> list[schemas.Tags]:
    event_id_int = int(event_id)
    db = get_db()
    query = (
        sa.select(models.Tags)
        .join(models.EventTag)
        .where(models.EventTag.event_id == event_id_int)
    )
    res = db.scalars(query)
    return [schemas.Tags.model_validate(tag) for tag in res.all()]


def crisis(event_id: str):
    event = get_event(event_id)
    if not event:
        st.error("Event not found")
        return

    event_owner = get_event_owner(event_id)
    if not event_owner:
        st.error("Event owner not found")
        return

    st.title(event.title)
    st.write(f"Location: {event.location}")

    st.write(f"Owner: {event_owner.name}")

    event_tags = get_event_tags(event_id)
    if event_tags:
        st.write("Tags: ", ", ".join([tag.text for tag in event_tags]))

    # img =
    # st.image(, use_column_width=True)

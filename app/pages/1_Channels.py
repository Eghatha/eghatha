import streamlit as st
from db.session import get_db
from db import models, schemas
import sqlalchemy as sa


def get_channels() -> list[schemas.Subscription]:
    db = get_db()
    query = sa.select(models.Subscription).order_by(
        models.Subscription.is_approved.desc()
    ).where(models.Subscription.user_id == 1)
    res = db.scalars(query)
    return [schemas.Subscription.model_validate(channel) for channel in res.all()]


def channels():
    st.title("Your Channels")

    channels = get_channels()

    if not channels:
        st.write("You are not subscribed to any channels.")
        return

    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown("## Title")
    with col2:
        st.markdown("## Date")
    with col3:
        st.markdown("## Location Name")
    with col4:
        st.markdown("## Status")

    for c in channels:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns(4, gap="large")
            with col1:
                st.markdown(f"**{c.event.title}**")
            with col2:
                st.write(c.created_at.date().isoformat())
            with col3:
                st.write(c.event.location)
            with col4:
                if c.is_approved:
                    st.link_button(
                        "Open", f"/?event_id={c.event_id}", use_container_width=True
                    )
                else:
                    st.write("Pending approval")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    channels()

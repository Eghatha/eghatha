import streamlit as st
from PIL import Image
from db.session import get_db
from db.models import User
import sqlalchemy as sa

im = Image.open("eghatha.jpg")

st.set_page_config(
    page_title="Eghatha",
    page_icon=im,
    layout="centered",
    initial_sidebar_state="expanded",
)


def home():
    db = get_db()
    q = sa.Select(User)
    res = db.scalars(q)
    res = res.all()
    st.title(res[0])

    st.map(
        data=None,
        zoom=15,
        use_container_width=True,
    )


home()

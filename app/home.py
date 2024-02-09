import streamlit as st
from PIL import Image

im = Image.open("eghatha.jpg")

st.set_page_config(
    page_title="Eghatha",
    page_icon=im,
    layout="centered",
    initial_sidebar_state="expanded",
)


def home():
    st.map(
        data=None,
        zoom=15,
        use_container_width=True,
    )


home()

import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
from crisis import crisis
from db.session import get_db
from db import models, schemas
import sqlalchemy as sa

im = Image.open("eghatha.jpg")

st.set_page_config(
    page_title="Eghatha",
    page_icon=im,
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extreme.com",
        "Report a bug": "https://www.extreme.com",
        "About": "https://www.extreme.com",
    },
)


def get_events() -> list[schemas.Event]:
    db = get_db()
    query = sa.select(models.Event)
    res = db.scalars(query)
    return [schemas.Event.model_validate(event) for event in res.all()]


def home():
    st.markdown("<center> <h1>Eghatha</h1> </center>", unsafe_allow_html=True)

    st.markdown(
        "<center> <h1>وَمَنْ أَحْيَاهَا فَكَأَنَّمَا أَحْيَا النَّاسَ جَمِيعًا</h1> </center>",
        unsafe_allow_html=True,
    )

    events = get_events()
    if not events:
        st.write("Oops.")
        return

    eventsMap = folium.Map(
        location=[31.4447, 34.3988],
        zoom_start=11,
    )

    for event in events:
        popup_content = f"<b>{event.title}</b><br>home destruction, injuries, ammunition needed<br><br><a href='/?event_id={event.id}' target='_blank'>KNOW MORE</a>"
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(
            location=[event.lat, event.lon],
            popup=popup,
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(eventsMap)

    st_folium(eventsMap, width=1000, height=700)


qp = st.query_params
if qp.get("event_id", None):
    crisis(qp["event_id"][0])
else:
    home()

import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium
from crisis import crisis


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


def home():
    map_type = st.sidebar.radio("Select Map Type", ("World", "Countries", "Continents"))

    # with st.expander("🧭 Menu"):
    #     st.page_link("home.py", label="Home", icon="🏠", use_container_width=True)
    #     st.page_link(
    #         "pages/dashboard.py",
    #         label="Dashboard",
    #         icon="2️⃣",
    #         use_container_width=True,
    #     )
    #     st.page_link(
    #         "pages/listings.py",
    #         label="Listings",
    #         icon="3️⃣",
    #         use_container_width=True,
    #     )
    #     st.page_link(
    #         "pages/stats.py",
    #         label="Stats",
    #         icon="4️⃣",
    #         use_container_width=True,
    #     )
    #     st.page_link(
    #         "pages/report.py",
    #         label="Report",
    #         icon="5️⃣",
    #         use_container_width=True,
    #     )

    # st.map(
    #     data=None,
    #     zoom=15,
    #     use_container_width=True,
    # )
    CircuitsMap = folium.Map(
        location=[31.4447, 34.3988],
        zoom_start=11,
    )
    folium.Marker(
        location=[31.4447, 34.3988],
        popup="Eghatha",
        icon=folium.Icon(color="red"),
    ).add_to(CircuitsMap)
    folium.Marker(
        location=[31.52806, 34.48306],
        popup="Eghatha",
        icon=folium.Icon(color="red"),
    ).add_to(CircuitsMap)

    # Add marker to the Folium map with custom popup

    crisis_areas = [
        {
            "location": [31.52806, 34.48306],
            "name": "Eghatha",
            "info": "Description of the crisis area.",
        },
        # Add more crisis areas as needed
    ]

    for area in crisis_areas:
        popup_content = f"<b>{area['name']}</b><br>{area['info']}<br><a href='https://www.google.com/maps?q={area['location'][0]},{area['location'][1]}' target='_blank'>Go to location</a>"
        popup = folium.Popup(popup_content, max_width=300)
        folium.Marker(
            location=area["location"],
            popup=popup,
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(CircuitsMap)

    st_folium(CircuitsMap, width=1000, height=800)


qp = st.query_params
if qp.get('event_id', None):
    crisis(qp['event_id'][0])
else:
    home()

import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium

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
        location=[31.5017, 34.4668],
        zoom_start=10.5,
    )
    st_folium(CircuitsMap)
    folium.Marker(
        location=[31.5017, 34.4668],
        popup="Eghatha",
        icon=folium.Icon(color="green"),
    ).add_to(CircuitsMap)


home()

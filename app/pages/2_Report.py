import streamlit as st
from streamlit_tags import st_tags
from db.session import get_db
from db import models
import random


def get_fale_lat_lon() -> tuple[float, float]:
    middle = (31.5017, 34.4668)
    return (
        middle[0] + random.uniform(-0.1, 0.1),
        middle[1] + random.uniform(-0.1, 0.1),
    )


def upload_report(
    *,
    title: str,
    location_name: str,
    needs: list[str],
    tags: list[str],
):
    db = get_db()
    lat, lon = get_fale_lat_lon()
    new_event = models.Event(
        title=title,
        location=location_name,
        lat=lat,
        lon=lon,
        criticality=3,
        created_by=1,
    )
    db.add(new_event)
    db.commit()

    for tag in tags:
        try:
            tag_obj = models.Tags(text=tag)
            db.add(tag_obj)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            continue

        rel = models.EventTag(event_id=new_event.id, tag_id=tag_obj.id)
        db.add(rel)
        db.commit()


def accident_report_form():
    st.title("Incident Reporting Form")

    # Name input
    title = st.text_input("Incident Title")

    location_name = st.text_input("Location Name")

    # Needs input
    needs = st_tags(
        label="Needs",
        text="Press enter to add a need",
        value=[],
        suggestions=[
            "doctor",
            "firefighter",
            "rescue team",
            "cars",
            "electrician",
            "clean water",
        ],
    )

    # Tags input
    tags = st_tags(
        label="Add tags",
        text="Press enter to add a tag",
        value=[],
        suggestions=["injury", "destruction", "ammunition"],
    )

    # Picture upload
    st.subheader("Upload Pictures of the Incident (optional)")
    uploaded_file = st.file_uploader(
        "Choose images", accept_multiple_files=False, type=["jpg", "jpeg", "png"]
    )

    # Submit button
    if st.button("Submit"):
        upload_report(
            title=title,
            location_name=location_name,
            needs=needs,
            tags=tags,
        )

        # Display submitted information
        st.success("Accident Reported!")


if __name__ == "__main__":
    accident_report_form()

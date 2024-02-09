import streamlit as st


def accident_report_form():
    st.title("Incident Reporting Form")

    # Name input
    name = st.text_input("Your Name")

    # Location input
    location = st.text_input("Location of Incident")

    # Needs input
    needs = st.text_area("Needs (e.g., medical assistance, police)")

    # Tags input
    tags = st.text_input("Tags (comma-separated)")

    # Picture upload
    st.subheader("Upload Pictures of the Incident (optional)")
    uploaded_files = st.file_uploader(
        "Choose images", accept_multiple_files=True, type=["jpg", "jpeg", "png"]
    )

    # Submit button
    if st.button("Submit"):
        # Saving uploaded images (if any)
        if uploaded_files:
            for i, file in enumerate(uploaded_files):
                with open(f"accident_{i}.jpg", "wb") as f:
                    f.write(file.getbuffer())

        # Display submitted information
        st.success("Accident Reported!")
        st.write(f"Name: {name}")
        st.write(f"Location: {location}")
        st.write(f"Needs: {needs}")
        st.write(f"Tags: {tags}")


if __name__ == "__main__":
    accident_report_form()

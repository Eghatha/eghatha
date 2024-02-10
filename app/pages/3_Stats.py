import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Dummy data for demonstration
volunteers_data = [
    {"Name": "John", "Volunteer Time (hrs)": 10, "Age": 25, "Gender": "Male"},
    {"Name": "Alice", "Volunteer Time (hrs)": 20, "Age": 30, "Gender": "Female"},
    {"Name": "Bob", "Volunteer Time (hrs)": 15, "Age": 40, "Gender": "Male"},
]


def stats_page():
    st.title("Stats")

    # Display number of volunteers joined
    num_volunteers = len(volunteers_data)
    st.subheader(f"Number of Volunteers Joined: {num_volunteers}")

    # Display number of users volunteered
    num_users_volunteered = sum(
        1 for volunteer in volunteers_data if volunteer["Volunteer Time (hrs)"] > 0
    )
    st.subheader(f"Number of Users Who Volunteered: {num_users_volunteered}")

    # Calculate average volunteer time
    if num_volunteers > 0:
        total_volunteer_time = sum(
            volunteer["Volunteer Time (hrs)"] for volunteer in volunteers_data
        )
        avg_volunteer_time = total_volunteer_time / num_volunteers
        st.subheader(f"Average Volunteer Time: {avg_volunteer_time:.2f} hours")

    # # Create pie chart for gender distribution
    # gender_df = pd.DataFrame(
    #     [{"Gender": volunteer["Gender"]} for volunteer in volunteers_data]
    # )
    # gender_fig = px.pie(gender_df, names="Gender", title="Gender Distribution")
    # st.plotly_chart(gender_fig)

    # Create histogram for volunteer time distribution
    volunteer_time_df = pd.DataFrame(
        [
            {"Volunteer Time (hrs)": volunteer["Volunteer Time (hrs)"]}
            for volunteer in volunteers_data
        ]
    )
    volunteer_time_fig = px.histogram(
        volunteer_time_df, x="Volunteer Time (hrs)", title="Volunteer Time Distribution"
    )
    st.plotly_chart(volunteer_time_fig)

    # Create scatter plot for volunteer time vs. age
    age_volunteer_time_df = pd.DataFrame(volunteers_data)
    age_volunteer_time_fig = px.scatter(
        age_volunteer_time_df,
        x="Age",
        y="Volunteer Time (hrs)",
        color="Gender",
        title="Volunteer Time vs. Age",
        trendline="ols",
    )
    st.plotly_chart(age_volunteer_time_fig)

    # Display volunteers data as a table
    volunteers_df = pd.DataFrame(volunteers_data)
    st.subheader("Volunteers Data:")
    st.write(volunteers_df)


if __name__ == "__main__":
    stats_page()

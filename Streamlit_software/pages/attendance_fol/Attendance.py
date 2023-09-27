import streamlit as st


st.set_page_config(page_title="Alliance Attendance Portal",page_icon="⚡")

st.title("Alliance Attendance Portal")
st.subheader("Attendance")


upload_col, analytics_col, penalty_col = st.columns(3)


with upload_col:
    upload_button = st.button("Upload Attendance")

with analytics_col:
    analytics_button = st.button("Attendance Analytics")

with penalty_col:
    penalty_button = st.button("Penalty")


if upload_button:
    pass

if analytics_button:
    pass

if penalty_button:
    PenaltyPage()


import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Alliance Attendance Portal",page_icon="⚡")

st.title("Alliance Attendance Portal")
st.subheader("Dashboard")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Select slot
    selected_slot = st.selectbox("Select Slot", os.listdir("Student_Attendance"))

    if not selected_slot:
        st.warning("First Select a Slot!")
with col2:
    # Select date
    selected_date = st.selectbox("Select a Date", ["17_09_23"] + os.listdir(f"Student_Attendance/{selected_slot}"))
    
    if selected_date == "Select a Date":
        st.warning("First Select a Date!")
        
with col3:
    # Select course (CSV file)
    if selected_slot and selected_date:
        if os.path.isdir(f"Student_Attendance/{selected_slot}/{selected_date}"):
            selected_course = st.selectbox("Select Course", ["Select a Course"] + [f for f in os.listdir(f"Student_Attendance/{selected_slot}/{selected_date}") if f.endswith(".csv")])
        if selected_course == "Select a Course":
            st.warning("First Select a Course!")


# Display attendance summary
if selected_course != "Select a Course":
    st.subheader("Attendance Summary")
    at_data = pd.read_csv(f"Student_Attendance/{selected_slot}/{selected_date}/{selected_course}")
    total_count = len(at_data)
    present_count = len(at_data[at_data["Attendance_Status"] == "Present"])
    absent_count = len(at_data[at_data["Attendance_Status"] == "Absent"])
    late_count = len(at_data[at_data["Attendance_Status"] == "Late"])
    excused_count = len(at_data[at_data["Attendance_Status"] == "Excused"])
    present_per = (present_count / total_count) * 100
    absent_per = (absent_count / total_count) * 100
    late_per = (late_count / total_count) * 100
    excused_per = (excused_count / total_count) * 100
    
    st.subheader("Total")
    st.write(f"{total_count} Students")


    st.write("### Attendance Graph\n")
    attendance_chart = pd.DataFrame(
        {
            'x_col':["1. Present","2. Absent","3. Late","4. Excused"],
            'y_col':[present_count, absent_count, late_count, excused_count],
        }
    )
    attendance_chart = attendance_chart.set_index("x_col")
    st.bar_chart(attendance_chart)
    # x = ["Present","Absent","Late","Excused"]
    # y = [present_count, absent_count, late_count, excused_count]
    # fig, ax = plt.subplots()
    # ax.plot(x,y)
    # plt.ylabel("Percentage")
    # st.pyplot(fig)
    

    st.write("\n")
    st.write("\n")
    
    col2, col3, col4, col5 = st.columns([1, 1, 1, 1])
    

    with col2:
        st.subheader("Present")
        st.write(f"{present_count} Students")
        present_student = f"{present_per:.2f}%"
        st.write(present_student)
    with col3:
        st.subheader("Absent")
        st.write(f"{absent_count} Students")
        absent_student = f"{absent_per:.2f}%"
        st.write(absent_student)
    with col4:
        st.subheader("Late")
        st.write(f"{late_count} Students")
        late_student = f"{late_per:.2f}%"
        st.write(late_student)
    with col5:
        st.subheader("Excused")
        st.write(f"{excused_count} Students")
        excused_student = f"{excused_per:.2f}%"
        st.write(excused_student) 
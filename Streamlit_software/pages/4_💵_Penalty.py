import streamlit as st
import pandas as pd

path_to_file = './Student_Penalty/penalty.csv'
df = pd.read_csv(path_to_file)

date = ['24_09_23','23_09_23','22_09_23','21_09_23','20_09_23','19_09_23']
slot = ['Slot A','Slot B','Slot C','Slot D']
room = ['345','200','105','113','627']
subject = ['CSE3002','CSE4033','CSE6001','CSE1045']
faculty = ['Ravi', 'Shanti', 'Mahesh', 'Maria']
reason = ['cell-phone', 'late', 'class-disturbance', 'property damage']

st.set_page_config(page_title="Alliance Attendance Portal",page_icon="⚡")

st.title("Alliance Attendance Portal")

st.subheader("Penalty")
st.write("\n")

st.write("Apply for penalty")
col_name, col_id = st.columns(2)

with col_name:
    student_name_input = st.text_input("Student name", "")

with col_id:
    student_id_input = st.text_input("Student ID", "")


col_date_sub, col_slot_fac, col_room_fine = st.columns(3)

with col_date_sub:
    date_option = st.selectbox('Date',date)
    
    subject_option = st.selectbox('Subject',subject)

with col_slot_fac:
    slot_option = st.selectbox('Slot',slot)
    
    faculty_option = st.selectbox('Faculty',faculty)

with col_room_fine:
    room_option = st.selectbox('Room',room)
    fine_option = st.selectbox('Reason',reason)

penalty = st.button("Generate Penalty")

if penalty:
    penalty = False
    df.loc[len(df.index)] = [date_option, student_name_input, student_id_input, slot_option, room_option,subject_option,faculty_option,fine_option] 
    df.to_csv(path_to_file, index=False)
    



search_by_id = st.text_input("Search by Student ID", "")
search = st.button("Search")
clear = st.button("clear")
if clear:
    search=False
    clear=False
    text = st.empty()

if search:
    df_new = df[df["student_id"] == search_by_id]
    st.dataframe(
        df_new,
        column_config={
            "date": "Date",
            "student_name": "Student name",
            "student_id": "Student ID",
            "slot": "Slot",
            "room": "Room no.",
            "subject": "Subject",
            "faculty": "Faculty",
            "reason": "Reason",
        },
        hide_index=True,
    )

else:
    st.dataframe(
        df,
        column_config={
            "date": "Date",
            "student_name": "Student name",
            "student_id": "Student ID",
            "slot": "Slot",
            "room": "Room no.",
            "subject": "Subject",
            "faculty": "Faculty",
            "reason": "Reason",
        },
        hide_index=True,
    )

# df = df.drop(df[df['product_name'] == 'Coca Cola'].index)







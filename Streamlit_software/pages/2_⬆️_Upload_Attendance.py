import streamlit as st
import pandas as pd
import os
import cv2
from deepface import DeepFace

date = ['25_09_23','24_09_23','23_09_23','22_09_23','21_09_23','20_09_23','19_09_23']
slot = ['Slot_A','Slot_B','Slot_C','Slot_D']
room = ['006','345','200','105','113','627']
subject = ['CSE1005','CSE3002','CSE4033','CSE6001','CSE1045']
faculty = ['Ravi', 'Shanti', 'Mahesh', 'Maria']

st.set_page_config(page_title="Alliance Attendance Portal",page_icon="⚡")

st.title("Alliance Attendance Portal")

st.subheader("Attendance Upload")

col_date_sub, col_slot_fac, col_room_fine = st.columns(3)

with col_date_sub:
    date_option = st.selectbox('Date',date)
    subject_option = st.selectbox('Subject',subject)

with col_slot_fac:
    slot_option = st.selectbox('Slot',slot)
    faculty_option = st.selectbox('Faculty',faculty)

with col_room_fine:
    room_option = st.selectbox('Room',room)

st.write("\n")
start_col, end_col = st.columns(2)

with start_col:
    img = st.file_uploader("Upload Start Video", type=['png','jpeg','jpg'])

with end_col:
    img_out = st.file_uploader("Upload End End", type=['png','jpeg','jpg'])


generate = st.button("Generate Report")

if generate:
    file_name = f'{date_option} {room_option} {subject_option} {faculty_option}.csv'
    path_to_file = f'./Student_Attendance/{slot_option}/{date_option}/{file_name}'
    df = pd.read_csv(path_to_file)
    path_to_save_photo = f'./Student_Attendance/{slot_option}/{date_option}/Attendance_photo/'
    
    file_detail_in = {"FileName":img.name, "FileType":img.type}
    path_to_img_in = os.path.join(path_to_save_photo, img.name)
    with open(path_to_img_in, "wb") as f:
        f.write(img.getbuffer())
    
    file_detail_out = {"FileName":img_out.name, "FileType":img_out.type}
    path_to_img_out= os.path.join(path_to_save_photo, img_out.name)
    with open(path_to_img_out, "wb") as f:
        f.write(img_out.getbuffer())



    present_class = cv2.imread(path_to_img_in) 
    attendance = []
    student_enrolled_path = f'./Student_Enrolled/{slot_option} {room_option} {subject_option}/'
    enrolled = os.listdir(student_enrolled_path)
    for student in enrolled:
        verification = DeepFace.verify(img1_path=os.path.join(student_enrolled_path, student), img2_path=present_class, model_name='ArcFace', detector_backend='retinaface')
        if verification['verified'] == True:
            attendance.append(student[:-4])
    
    print(attendance)
    for student_id in attendance:
        index = df[df['Student_id'] == student_id].index
        df.loc[df['Student_id'] == student_id, 'Attendance_Status'] = 'Present'


    present_class = cv2.imread(path_to_img_out) 
    attendance = []
    student_enrolled_path = f'./Student_Enrolled/{slot_option} {room_option} {subject_option}/'
    enrolled = os.listdir(student_enrolled_path)
    for student in enrolled:
        verification = DeepFace.verify(img1_path=os.path.join(student_enrolled_path, student), img2_path=present_class, model_name='ArcFace', detector_backend='retinaface')
        if verification['verified'] == True:
            attendance.append(student[:-4])
    
    print(attendance)
    for student_id in attendance:
        df.loc[(df['Student_id'] == student_id) & (df['Attendance_Status'] == 'Absent'), 'Attendance_Status'] = 'Late'

    
    df.to_csv(path_to_file, index=False)

    st.dataframe(
        df,
        column_config={
            "Student_name": "Student name",
            "Student_id": "Student ID",
            "Attendance_Status": "Attendance Status",
            
        },
        hide_index=True,
    )
    generate=False

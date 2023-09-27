import streamlit as st
import pandas as pd
import os
import cv2
from ultralytics import YOLO
import random
from PIL import Image

model = YOLO("./m]Model/yolov8n.pt")

date = ['25_09_23','24_09_23','23_09_23','22_09_23','21_09_23','20_09_23','19_09_23']
slot = ['Slot_A','Slot_B','Slot_C','Slot_D']
room = ['006','345','200','105','113','627']
subject = ['CSE1005','CSE3002','CSE4033','CSE6001','CSE1045']
faculty = ['Ravi', 'Shanti', 'Mahesh', 'Maria']

st.set_page_config(page_title="Alliance Attendance Portal",page_icon="⚡")

st.title("Alliance Attendance Portal")

st.subheader("Check if Anomaly")


col_date_sub, col_slot_fac, col_room_fine = st.columns(3)

with col_date_sub:
    date_option = st.selectbox('Date',date)
    subject_option = st.selectbox('Subject',subject)

with col_slot_fac:
    slot_option = st.selectbox('Slot',slot)
    faculty_option = st.selectbox('Faculty',faculty)

with col_room_fine:
    room_option = st.selectbox('Room',room)

vid = st.file_uploader("Upload Video")


generate = st.button("Generate Report")

if generate:
    i=0
    
    file_detail = {"FileName":vid.name, "FileType":vid.type}
    path_to_save_vid = f'./Student_Attendance/{slot_option}/{date_option}/Anomaly/'
    path_to_vid = os.path.join(path_to_save_vid, vid.name)
    
    detect_img_path = f'{path_to_save_vid}/pic/'
    with open(path_to_vid, "wb") as f:
        f.write(vid.getbuffer())
    
    cap = cv2.VideoCapture(path_to_vid)
    while cap.isOpened():
        success, frame = cap.read()
        # frame = cv2.resize(frame, (640, 360))
        if success:

            results = model.predict(source=frame, classes=[67], boxes=True, save_conf=True)
            annotated_frame = results[0].plot(line_width=1)

            if len(results[0].boxes.cls) > 0:  
                file_dir=f'{detect_img_path}{vid.name}{i}.jpg'
                cv2.imwrite(file_dir, annotated_frame)    
                i+=1                                       
                
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    
    list_of_detects = os.listdir(detect_img_path)
    path_to_display = []
    for i in range(0,5):
        random_file = list_of_detects [random.randint(1, len(list_of_detects))]
        temp_path = f'{detect_img_path}{random_file}'
        path_to_display.append(temp_path)
    
    image1 = Image.open(path_to_display[0])
    image2 = Image.open(path_to_display[1])
    image3 = Image.open(path_to_display[2])
    image4 = Image.open(path_to_display[3])

    st.image(image1, caption='Phone detected')
    st.image(image2, caption='Phone detected')
    st.image(image3, caption='Phone detected')
    st.image(image4, caption='Phone detected')
    
    cap.release()
import face_recognition
import cv2
import os
import pandas as pd
from datetime import datetime

path="images"

known_encodings=[]
known_names=[]
marked=[]
for folder in os.listdir(path):
    folder_path=os.path.join(path,folder)
    for img_name in os.listdir(folder_path):
        img_path=os.path.join(folder_path,img_name)
        img=face_recognition.load_image_file(img_path)
        encodings=face_recognition.face_encodings(img)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(folder)
print("encoding complete")

cap=cv2.VideoCapture(0)
def mark_attendance(name):
    now=datetime.now()
    time=now.strftime("%H:%M:%S")
    
    file_path="attendance/attendance.csv"
    try:
        df=pd.read_csv(file_path)
    except:
        df=pd.DataFrame(columns=["Name","Time"])
    if name not in df["Name"].values:
        new_row={"Name":name,"Time":time}
        df=pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(file_path,index=False)
        print("Attendance Saved:",name)

process =True

while True:
    ret,frame=cap.read()
    if  not ret:
        print("Camera error")
        break

    small_frame=cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb=cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
    if process:
     faces=face_recognition.face_locations(rgb)
     #print("Faces:", len(faces))
     encodes=face_recognition.face_encodings(rgb,faces)
     #print("Encodes:", len(encodes))
     name="Unknown"
     for encode in encodes:
        name="Unknown"
        matches=face_recognition.compare_faces(known_encodings,encode)
        if True in matches:
            index=matches.index(True)
            name=known_names[index]
            if name not in marked:
                mark_attendance(name)
                marked.append(name)
        else:
            print("Unknown")
        cv2.putText(frame,name,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow("Recognition",frame)
    
    if cv2.waitKey(1)==27:
        break
    process=not process
cap.release()
cv2.destroyAllWindows()
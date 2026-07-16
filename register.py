import cv2
import os

cap=cv2.VideoCapture(0)

student_id=input("Enter Student ID: ")
name=input("Enter Name :")

folder_path=f"images/{name}_{student_id}"
os.makedirs(folder_path,exist_ok=True)

count=0

while True:
    ret,frame=cap.read()
    
    if not ret:
        print("Camera error")
        break
    cv2.imshow("Capture Faces",frame)

    key=cv2.waitKey(1)
    if key==ord('c'):
        img_path=f"{folder_path}/{count}.jpg"
        cv2.imwrite(img_path,frame)
        count+=1
        print("Captured image: ",count)
    if key ==27:
        break
    if count>=20:
        break
cap.release()
cv2.destroyAllWindows()

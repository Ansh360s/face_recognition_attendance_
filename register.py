import cv2
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

cap=cv2.VideoCapture(0)

student_id=input("Enter Student ID: ")
name=input("Enter Name :")

#database connection
student_id=int(student_id)
connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor=connection.cursor()
cursor.execute('INSERT INTO students (student_id,"NAME") VALUES (%s, %s)', (student_id, name))
connection.commit()
cursor.close()
connection.close()
print("Student added to the database successfully.")



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

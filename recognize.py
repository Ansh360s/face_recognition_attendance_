import os
import cv2
import face_recognition
import psycopg
from datetime import datetime
from zoneinfo import ZoneInfo
from export_attendance import export_attendance
from dotenv import load_dotenv

load_dotenv()

IMAGE_PATH = "images"



def load_known_faces():
    known_encodings = []
    known_students = []

    for folder_name in os.listdir(IMAGE_PATH):
        folder_path = os.path.join(IMAGE_PATH, folder_name)
        if not os.path.isdir(folder_path):
            continue
        try:
            _,student_id = folder_name.rsplit("_", 1)  
        except ValueError:
            print(f"Skipping folder '{folder_name}' as it does not follow the expected naming convention.")
            continue

        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                name = get_student_name(student_id)  # Fetch the name from the database
                known_students.append((student_id, name))

    return known_encodings, known_students


def get_student_name(student_id):
    connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

    cursor = connection.cursor()
    cursor.execute('SELECT "NAME" FROM students WHERE student_id = %s', (student_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return result[0]
    return "Unknown"


def mark_attendance(student_id, name):
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    current_time = now.time().replace(tzinfo=None)  # Remove timezone info for database storage
    current_date = now.date()
    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cursor = connection.cursor()
    cursor.execute('SELECT attendance_id FROM attendance WHERE student_id = %s AND attendance_date = %s', (student_id, current_date))
    already_marked = cursor.fetchone()
    if already_marked:
        print(f"Attendance already marked for {name} on {current_date}.")
    else:
        cursor.execute('INSERT INTO attendance (student_id, attendance_date, attendance_time,status) VALUES (%s, %s, %s, %s)', (student_id, current_date, current_time,"Present"))
        connection.commit()
        print(f"Attendance marked for {name}_{student_id} at {current_time} on {current_date}.")
        export_attendance()  # Call the export function after marking attendance

    cursor.close()
    connection.close()



def main():
    known_encodings, known_students = load_known_faces()

    if not known_encodings:
        print("No known faces found.")
        return

    cap = cv2.VideoCapture(0)
    marked = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera error")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)

            if True in matches:
                index = matches.index(True)
                student_id, name = known_students[index]
                if student_id not in marked:
                    mark_attendance(student_id, name)
                    marked.append(student_id)
            else:
                name = "Unknown"

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

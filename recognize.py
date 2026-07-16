import os
import cv2
import face_recognition
import pandas as pd
from datetime import datetime

IMAGE_PATH = "images"
ATTENDANCE_FILE = "attendance/attendance.csv"


def load_known_faces():
    known_encodings = []
    known_names = []

    for folder_name in os.listdir(IMAGE_PATH):
        folder_path = os.path.join(IMAGE_PATH, folder_name)
        if not os.path.isdir(folder_path):
            continue

        for image_name in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(folder_name)

    return known_encodings, known_names


def mark_attendance(name):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    os.makedirs(os.path.dirname(ATTENDANCE_FILE), exist_ok=True)

    if os.path.exists(ATTENDANCE_FILE):
        df = pd.read_csv(ATTENDANCE_FILE)
    else:
        df = pd.DataFrame(columns=["Name", "Time"])

    if name not in df["Name"].values:
        new_row = {"Name": name, "Time": current_time}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(ATTENDANCE_FILE, index=False)
        print("Attendance saved:", name)


def main():
    known_encodings, known_names = load_known_faces()

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
                name = known_names[index]
                if name not in marked:
                    mark_attendance(name)
                    marked.append(name)
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

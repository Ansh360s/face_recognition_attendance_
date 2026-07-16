# Face Recognition Attendance System

A Face Recognition Attendance System built using Python, OpenCV, face_recognition, and dlib.

## Features

- Register new students
- Capture 20 face images per student
- Face recognition using webcam
- Automatic attendance marking
- Attendance stored in CSV
- View attendance records
- Clear attendance records

## Technologies Used

- Python 3.10
- OpenCV
- face_recognition
- dlib
- NumPy
- Pandas

## Project Structure

```
Face_Attendance/
│
├── images/
├── attendance/
├── register.py
├── recognize.py
├── attendance.py
├── test_camera.py
├── README.md
```

## How to Run

Install dependencies

```bash
pip install opencv-python
pip install face_recognition
pip install pandas
pip install numpy
```

Register a student

```bash
python register.py
```

Recognize faces

```bash
python recognize.py
```

## Future Improvements

- GUI
- Database
- Admin Login
- Excel Export
- Real-time CCTV Support
- Deep Learning Face Recognition
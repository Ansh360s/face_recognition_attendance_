# Face Recognition Attendance System

A Face Recognition Attendance System built using Python, OpenCV, face_recognition, PostgreSQL, and Pandas.

The system allows students to be registered with their Student ID and name, captures face images, recognizes students through a webcam, and automatically records attendance in a PostgreSQL database.

## Features

- Register new students
- Capture 20 face images per student
- Face recognition using webcam
- Automatic attendance marking
- Prevent duplicate attendance on the same day
- Store student information in PostgreSQL
- Store attendance records in PostgreSQL
- Generate attendance report in Excel
- Export attendance with student name, ID, date, time, and status
- Use `.env` file for database credentials
- Keep personal face images and attendance files private using `.gitignore`

## Technologies Used

- Python 3.10
- OpenCV
- face_recognition
- dlib
- NumPy
- Pandas
- PostgreSQL
- psycopg
- openpyxl
- python-dotenv
- Git & GitHub

## Project Structure

```text
Face_Attendance/
│
├── images/                  # Student face images (local only)
├── attendance/              # Old attendance files / project data
│
├── register.py              # Register students and capture face images
├── recognize.py             # Face recognition and attendance marking
├── database.py              # PostgreSQL database connection
├── export_attendance.py     # Export attendance to Excel
├── test_encoding.py         # Face encoding testing
│
├── .env                     # Database credentials (NOT uploaded)
├── .gitignore               # Files excluded from Git
├── README.md
└── attendance.xlsx          # Generated locally (NOT uploaded)


Database
The project uses PostgreSQL to store student and attendance information.
Students Table
Stores:
Student ID
Student Name
Attendance Table
Stores:
Attendance ID
Student ID
Attendance Date
Attendance Time
Attendance Status
The Student ID is used to connect student information with attendance records.
Setup
1. Clone the repository

git clone YOUR_REPOSITORY_URL
cd Face_Attendance

2. Create the Python environment
Python 3.10 is recommended.
Install the required libraries:

pip install opencv-python
pip install face_recognition
pip install pandas
pip install numpy
pip install psycopg[binary]
pip install openpyxl
pip install python-dotenv

3. Configure the database
Create a PostgreSQL database named:
attendance_system

Create a .env file in the project folder:
DB_HOST=localhost
DB_NAME=attendance_system
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD

Do not upload the .env file to GitHub.
How to Run
Register a student
python register.py

Enter the Student ID and name when prompted.
The system captures face images and stores them locally.
Start face recognition
python recognize.py

The webcam will detect and recognize registered students.
When a student is recognized, attendance is automatically recorded in PostgreSQL.
Export Attendance
python export_attendance.py

This generates:

attendance.xlsx

The Excel report contains:
Attendance ID
Student ID
Student Name
Attendance Date
Attendance Time
Status
Privacy
Student face images and attendance records contain personal information.
The following files are intentionally excluded from GitHub:
.env
images/
attendance.xlsx
*.xlsx

Database passwords should never be stored directly inside Python source code.

Current Workflow
Student Registration
        ↓
Capture Face Images
        ↓
Store Student Information
        ↓
PostgreSQL Database
        ↓
Face Recognition
        ↓
Identify Student
        ↓
Check Today's Attendance
        ↓
Mark Attendance
        ↓
Export Attendance to Excel

Future Improvements
GUI-based application
Admin login
Attendance dashboard
Better face recognition accuracy
Multiple camera/CCTV support
Attendance analytics
Search and filter attendance
Student management system
Improved error handling
Deep learning based face recognition
Deployment as a complete application
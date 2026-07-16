import os
import pandas as pd

ATTENDANCE_FILE = "attendance/attendance.csv"


def load_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return pd.DataFrame(columns=["Name", "Time"])
    return pd.read_csv(ATTENDANCE_FILE)


def show_attendance():
    df = load_attendance()

    if df.empty:
        print("No attendance marked yet.")
    else:
        print(df.to_string(index=False))


def clear_attendance():
    os.makedirs(os.path.dirname(ATTENDANCE_FILE), exist_ok=True)
    df = pd.DataFrame(columns=["Name", "Time"])
    df.to_csv(ATTENDANCE_FILE, index=False)
    print("Attendance file cleared.")


def main():
    while True:
        print("\n1. View attendance")
        print("2. Clear attendance")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            show_attendance()
        elif choice == "2":
            clear_attendance()
        elif choice == "3":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

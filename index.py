# from flask import Flask, render_template, request, redirect, url_for, flash, Response
# import json
# import os
# import csv
# import io
# from datetime import date

# app = Flask(__name__)
# app.secret_key = "attendance_system_secret_key"
# FILE_NAME = "attendance.json"

# DEFAULT_DATA = {
#     "101": {
#         "name": "Aarav Sharma",
#         "attendance": {
#             "2026-11-16": "P",
#             "2026-11-17": "P",
#             "2026-11-18": "A",
#             "2026-11-19": "P",
#             "2026-11-20": "P"
#         }
#     },
#     "102": {
#         "name": "Priya Patel",
#         "attendance": {
#             "2026-11-16": "P",
#             "2026-11-17": "P",
#             "2026-11-18": "P",
#             "2026-11-19": "P",
#             "2026-11-20": "P"
#         }
#     },
#     "103": {
#         "name": "Rohan Verma",
#         "attendance": {
#             "2026-11-16": "A",
#             "2026-11-17": "A",
#             "2026-11-18": "P",
#             "2026-11-19": "A",
#             "2026-11-20": "P"
#         }
#     },
#     "104": {
#         "name": "Ananya Iyer",
#         "attendance": {
#             "2026-11-16": "P",
#             "2026-11-17": "A",
#             "2026-11-18": "P",
#             "2026-11-19": "P"
#         }
#     },
#     "105": {
#         "name": "Kabir Singh",
#         "attendance": {
#             "2026-11-16": "P",
#             "2026-11-17": "P",
#             "2026-11-18": "P",
#             "2026-11-19": "A"
#         }
#     }
# }


# def load_data():
#     if not os.path.exists(FILE_NAME):
#         save_data(DEFAULT_DATA)
#         return DEFAULT_DATA
#     with open(FILE_NAME, "r") as file:
#         try:
#             return json.load(file)
#         except json.JSONDecodeError:
#             return {}


# def save_data(data):
#     with open(FILE_NAME, "w") as file:
#         json.dump(data, file, indent=4)


# @app.route("/")
# def index():
#     students = load_data()
#     today = str(date.today())
    
#     student_stats = {}
#     for roll, details in students.items():
#         records = details.get("attendance", {})
#         # Sort records chronologically by date
#         sorted_records = dict(sorted(records.items()))
#         total = len(sorted_records)
#         present = list(sorted_records.values()).count("P")
#         absent = total - present
#         percentage = round((present / total) * 100, 2) if total > 0 else 0.0
        
#         student_stats[roll] = {
#             "name": details["name"],
#             "records": sorted_records,
#             "total": total,
#             "present": present,
#             "absent": absent,
#             "percentage": percentage,
#             "today_status": sorted_records.get(today, "Not Marked")
#         }

#     return render_template("index.html", students=student_stats, today=today)


# @app.route("/add_student", methods=["POST"])
# def add_student():
#     roll = request.form.get("roll", "").strip()
#     name = request.form.get("name", "").strip()
#     students = load_data()

#     if not roll or not name:
#         flash("Roll number and name are required!", "error")
#     elif roll in students:
#         flash(f"Roll number {roll} already exists!", "error")
#     else:
#         students[roll] = {
#             "name": name,
#             "attendance": {}
#         }
#         save_data(students)
#         flash(f"Added {name} (Roll: {roll}) successfully!", "success")

#     return redirect(url_for("index"))


# @app.route("/mark_attendance", methods=["POST"])
# def mark_attendance():
#     roll = request.form.get("roll")
#     status = request.form.get("status")
#     selected_date = request.form.get("date") or str(date.today())
    
#     students = load_data()

#     if roll in students and status in ["P", "A"]:
#         students[roll]["attendance"][selected_date] = status
#         save_data(students)
#         label = "Present" if status == "P" else "Absent"
#         flash(f"Marked {label} for {students[roll]['name']} ({selected_date}).", "success")
#     else:
#         flash("Invalid student or status!", "error")

#     return redirect(url_for("index"))


# @app.route("/delete_student/<roll>", methods=["POST"])
# def delete_student(roll):
#     students = load_data()
#     if roll in students:
#         removed_name = students.pop(roll)["name"]
#         save_data(students)
#         flash(f"Deleted student {removed_name} (Roll: {roll}).", "success")
#     else:
#         flash("Student not found!", "error")
#     return redirect(url_for("index"))


# @app.route("/export_csv")
# def export_csv():
#     students = load_data()
#     output = io.StringIO()
#     writer = csv.writer(output)
    
#     writer.writerow(["Roll Number", "Name", "Total Classes", "Present", "Absent", "Attendance %"])
    
#     for roll, details in students.items():
#         records = details.get("attendance", {})
#         total = len(records)
#         present = list(records.values()).count("P")
#         absent = total - present
#         percentage = round((present / total) * 100, 2) if total > 0 else 0.0
#         writer.writerow([roll, details["name"], total, present, absent, f"{percentage}%"])
        
#     return Response(
#         output.getvalue(),
#         mimetype="text/csv",
#         headers={"Content-Disposition": "attachment;filename=attendance_report.csv"}
#     )


# if __name__ == "__main__":
#     app.run(debug=True)
import json
import os
from datetime import date

FILE_NAME = "attendance.json"


def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


students = load_data()


def add_student():
    roll = input("Enter Roll Number: ")
    name = input("Enter Student Name: ")

    if roll in students:
        print("Student already exists!")
    else:
        students[roll] = {
            "name": name,
            "attendance": {}
        }
        save_data(students)
        print("Student added successfully!")


def view_students():
    if not students:
        print("No students found.")
        return

    print("\n--- Student List ---")

    for roll, details in students.items():
        print(f"Roll: {roll} | Name: {details['name']}")


def mark_attendance():
    roll = input("Enter Roll Number: ")

    if roll not in students:
        print("Student not found!")
        return

    status = input("Enter P for Present or A for Absent: ").upper()

    if status not in ["P", "A"]:
        print("Invalid attendance status!")
        return

    today = str(date.today())

    students[roll]["attendance"][today] = status

    save_data(students)

    print("Attendance marked successfully!")


def view_attendance():
    roll = input("Enter Roll Number: ")

    if roll not in students:
        print("Student not found!")
        return

    print("\nName:", students[roll]["name"])
    print("--- Attendance Records ---")

    records = students[roll]["attendance"]

    for day, status in records.items():
        print(day, "-", "Present" if status == "P" else "Absent")


def attendance_percentage():
    roll = input("Enter Roll Number: ")

    if roll not in students:
        print("Student not found!")
        return

    records = students[roll]["attendance"]

    total = len(records)
    present = list(records.values()).count("P")

    if total == 0:
        print("No attendance records found.")
        return

    percentage = (present / total) * 100

    print("Student:", students[roll]["name"])
    print("Total Classes:", total)
    print("Present:", present)
    print("Absent:", total - present)
    print(f"Attendance Percentage: {percentage:.2f}%")


# Main Menu

while True:

    print("\n===== STUDENT ATTENDANCE MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Mark Attendance")
    print("4. View Attendance")
    print("5. Attendance Percentage")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        mark_attendance()

    elif choice == "4":
        view_attendance()

    elif choice == "5":
        attendance_percentage()

    elif choice == "6":
        print("Thank you for using the system!")
        break

    else:
        print("Invalid choice! Please try again.")
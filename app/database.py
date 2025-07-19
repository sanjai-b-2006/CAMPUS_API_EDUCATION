import json
import os

# 👇 Adjust path for safe cross-platform use
COURSES_PATH = os.path.join(r"C:\Users\sanja\Desktop\hackathon\API_development\2\college_api\mock_data", "courses.json")
FACULTY_PATH = os.path.join(r"C:\Users\sanja\Desktop\hackathon\API_development\2\college_api\mock_data", "faculty.json")

with open(COURSES_PATH, "r") as f:
    courses = json.load(f)

with open(FACULTY_PATH, "r") as f:
    faculty = json.load(f)

def get_course(course_id):
    return next((c for c in courses if c["id"] == course_id), None)

def get_faculty(faculty_id):
    return next((f for f in faculty if f["id"] == faculty_id), None)

def save_courses():
    with open(COURSES_PATH, "w") as f:
        json.dump(courses, f, indent=2)

def save_faculty():
    with open(FACULTY_PATH, "w") as f:
        json.dump(faculty, f, indent=2)

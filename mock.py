import json
from faker import Faker
import random

fake = Faker()
departments = ["CSE", "ECE", "Mechanical", "AI", "Smart Manufacturing"]
specializations = {
    "CSE": ["ML", "AI", "Security", "DBMS"],
    "ECE": ["VLSI", "Embedded", "Signal Processing"],
    "Mechanical": ["Thermodynamics", "Fluid Mechanics"],
    "AI": ["Neural Nets", "Deep Learning", "NLP"],
    "Smart Manufacturing": ["Automation", "3D Printing", "Robotics"]
}
faculty = []
for i in range(1, 101):
    dept = random.choice(departments)
    faculty.append({
        "id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "department": dept,
        "specialization": random.sample(specializations[dept], 2),
        "office_location": f"Room {random.randint(100, 199)}",
        "office_hours": f"{random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])}/"
                        f"{random.choice(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'])} "
                        f"{random.randint(9, 16)}:00-{random.randint(17, 20)}:00"
    })

with open("faculty.json", "w") as f:
    json.dump(faculty, f, indent=2)
courses = []
for i in range(101, 201):
    dept = random.choice(departments)
    fid = random.randint(1, 100)
    prereq = [random.randint(101, 120) for _ in range(random.randint(0, 3))]
    courses.append({
        "id": i,
        "name": fake.catch_phrase(),
        "code": f"{dept[:2].upper()}{random.randint(100,499)}",
        "description": f"This course covers fundamentals of {fake.word()} in {dept} department.",
        "credits": random.choice([2, 3, 4]),
        "department": dept,
        "prerequisites": prereq,
        "faculty_id": fid
    })

with open("courses.json", "w") as f:
    json.dump(courses, f, indent=2)

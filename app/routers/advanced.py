from fastapi import APIRouter, Query
from database import courses, faculty
from collections import Counter

router = APIRouter(prefix="/advanced", tags=["Advanced Features"])

@router.get("/courses/by-credits/")
def courses_by_credit(min_credit: int = 3):
    return [c for c in courses if c["credits"] >= min_credit]

@router.get("/faculty/available-on/")
def faculty_by_office_hours(day: str):
    return [prof for prof in faculty if day.lower() in prof["office_hours"].lower()]

@router.get("/courses/search/")
def course_search(query: str):
    q = query.lower()
    return [c for c in courses if q in c["name"].lower() or q in c["description"].lower()]

@router.get("/analytics/faculty-course-load")
def faculty_course_load():
    counts = Counter(c["faculty_id"] for c in courses)
    top = counts.most_common(1)
    top_faculty = next((f for f in faculty if f["id"] == top[0][0]), None)
    return {
        "max_courses": top[0][1],
        "faculty": {
            "id": top_faculty["id"],
            "name": f"{top_faculty['first_name']} {top_faculty['last_name']}",
            "email": top_faculty["email"]
        }
    }

@router.get("/faculty/specialization/")
def find_by_specialization(topic: str):
    topic = topic.lower()
    return [
        f for f in faculty if any(topic in s.lower() for s in f["specialization"])
    ]

@router.get("/courses/with-faculty/")
def get_courses_with_faculty():
    enriched = []
    for c in courses:
        f = next((f for f in faculty if f["id"] == c["faculty_id"]), None)
        if f:
            c_copy = c.copy()
            c_copy["faculty_details"] = f
            enriched.append(c_copy)
    return enriched

@router.get("/search/all")
def search_all(query: str):
    q_lower = query.lower()
    course_results = [c for c in courses if q_lower in c["name"].lower() or q_lower in c["description"].lower() or q_lower in c["code"].lower()]
    faculty_results = [f for f in faculty if q_lower in f["first_name"].lower() or q_lower in f["last_name"].lower() or any(q_lower in s.lower() for s in f["specialization"])]
    return {"courses": course_results, "faculty": faculty_results}

@router.get("/departments/course-count")
def department_course_count():
    counts = {}
    for c in courses:
        dept = c["department"]
        counts[dept] = counts.get(dept, 0) + 1
    return counts

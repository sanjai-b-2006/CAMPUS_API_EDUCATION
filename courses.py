from fastapi import APIRouter, HTTPException, Query, Body
from models import Course
from database import faculty, courses, save_courses
from difflib import get_close_matches

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/search")
def search_courses(query: str = Query(..., description="Search across all course fields")):
    # Search all fields for the query
    q = query.lower()
    result = []
    for c in courses:
        if (
            q in str(c.get("id", "")).lower()
            or q in c.get("name", "").lower()
            or q in c.get("code", "").lower()
            or q in c.get("description", "").lower()
            or q in c.get("department", "").lower()
            or q in str(c.get("credits", "")).lower()
            or any(q in str(pr) for pr in c.get("prerequisites", []))
            or q in str(c.get("faculty_id", "")).lower()
        ):
            result.append(c)
    return result

@router.get("/", response_model=list[Course])
def get_courses(limit: int = 10, offset: int = 0, sort_by: str = "id", order: str = "asc"):
    allowed = ["id", "name", "code", "credits"]
    if sort_by not in allowed:
        raise HTTPException(400, f"Can only sort by {allowed}")
    sorted_courses = sorted(courses, key=lambda x: x[sort_by])
    if order == "desc":
        sorted_courses.reverse()
    return sorted_courses[offset: offset + limit]

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    course = next((c for c in courses if c["id"] == course_id), None)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=Course)
def create_course(course: Course):
    if any(c["id"] == course.id for c in courses):
        raise HTTPException(400, detail="Course ID already exists")
    courses.append(course.dict())
    save_courses()
    return course

@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, updated: Course):
    for i, c in enumerate(courses):
        if c["id"] == course_id:
            courses[i] = updated.dict()
            save_courses()
            return updated
    raise HTTPException(status_code=404, detail="Course not found")

@router.delete("/{course_id}")
def delete_course(course_id: int):
    global courses
    courses = [c for c in courses if c["id"] != course_id]
    save_courses()
    return {"message": "Course deleted"}

@router.patch("/{course_id}")
def update_course_partial(course_id: int, updates: dict = Body(...)):
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        raise HTTPException(404, "Course not found")
    for key, value in updates.items():
        if key in course:
            course[key] = value
    save_courses()
    return course

# All advanced course analytics and searching features:
@router.get("/courses/{course_id}/prerequisites/full")
def get_prerequisite_chain(course_id: int):
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        raise HTTPException(404, "Course not found")
    result = []
    for pre_id in course["prerequisites"]:
        pre_course = next((c for c in courses if c["id"] == pre_id), None)
        if pre_course:
            pre_fac = next((f for f in faculty if f["id"] == pre_course["faculty_id"]), None)
            result.append({
                "course_id": pre_course["id"],
                "course_code": pre_course["code"],
                "course_name": pre_course["name"],
                "faculty_id": pre_fac["id"] if pre_fac else None,
                "faculty_name": f"{pre_fac['first_name']} {pre_fac['last_name']}" if pre_fac else None,
                "faculty_email": pre_fac["email"] if pre_fac else None
            })
    return {"course": course["name"], "prerequisites": result}

@router.get("/courses/most-prerequisites")
def top_courses_most_prerequisites(top: int = 5):
    sorted_courses = sorted(courses, key=lambda c: len(c["prerequisites"]), reverse=True)
    return sorted_courses[:top]

@router.get("/courses/no-prerequisites")
def courses_no_prerequisites():
    return [c for c in courses if not c["prerequisites"]]

@router.get("/courses/by-semester/{semester}")
def courses_by_semester(semester: str):
    return [c for c in courses if c.get("semester") and c["semester"].lower() == semester.lower()]

@router.get("/courses/specialization")
def courses_by_specializations(topics: str = Query(..., description="Comma separated specializations")):
    topic_list = [t.strip().lower() for t in topics.split(",")]
    matched_courses = []
    for c in courses:
        fac = next((f for f in faculty if f["id"] == c["faculty_id"]), None)
        if fac and all(any(topic in spec.lower() for spec in fac["specialization"]) for topic in topic_list):
            matched_courses.append(c)
    return matched_courses

@router.get("/courses/{course_id}/prerequisite-path")
def recursive_prerequisite_path(course_id: int):
    def recurse(c_id, visited):
        if c_id in visited:
            return []
        visited.add(c_id)
        course = next((c for c in courses if c["id"] == c_id), None)
        if not course:
            return []
        path = []
        for pre_id in course["prerequisites"]:
            path.extend(recurse(pre_id, visited))
        path.append(course)
        return path
    path_list = recurse(course_id, set())
    return [{"id": c["id"], "name": c["name"]} for c in path_list]

@router.get("/courses/match-interest")
def courses_match_interest(fields: str = Query(..., description="Comma separated interest fields")):
    interest_list = [f.strip().lower() for f in fields.split(",")]
    matched = []
    for c in courses:
        fac = next((f for f in faculty if f["id"] == c["faculty_id"]), None)
        desc_match = any(field in c["description"].lower() for field in interest_list)
        spec_match = fac and any(any(field in spec.lower() for spec in fac["specialization"]) for field in interest_list)
        if desc_match or spec_match:
            matched.append(c)
    return matched

@router.get("/courses/recommend")
def recommend_courses(interests: str):
    terms = [i.strip().lower() for i in interests.split(",")]
    result = []
    for c in courses:
        fac = next((f for f in faculty if f["id"] == c["faculty_id"]), None)
        if any(term in c["description"].lower() for term in terms) or (
            fac and any(term in s.lower() for s in fac["specialization"] for term in terms)
        ):
            result.append(c)
    return result

@router.get("/courses/fuzzy")
def fuzzy_course_search(term: str, threshold: int = 80):
    names = [c["name"] for c in courses]
    matches = get_close_matches(term, names, cutoff=threshold / 100.0)
    return [c for c in courses if c["name"] in matches]

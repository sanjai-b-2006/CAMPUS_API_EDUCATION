from fastapi import APIRouter, HTTPException, Query, Body
from models import Faculty
from difflib import get_close_matches
from database import save_faculty, courses, faculty

router = APIRouter(prefix="/faculty", tags=["Faculty"])

@router.get("/", response_model=list[Faculty])
def get_all_faculty():
    return faculty

@router.get("/{faculty_id}", response_model=Faculty)
def get_faculty_by_id(faculty_id: int):
    member = next((f for f in faculty if f["id"] == faculty_id), None)
    if member is None:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return member

@router.post("/", response_model=Faculty, status_code=201)
def add_faculty(new_faculty: Faculty):
    if any(f["id"] == new_faculty.id for f in faculty):
        raise HTTPException(status_code=400, detail="Faculty with this ID already exists.")
    faculty.append(new_faculty.dict())
    save_faculty()
    return new_faculty

@router.put("/{faculty_id}", response_model=Faculty)
def update_faculty(faculty_id: int, updated: Faculty):
    for i, f in enumerate(faculty):
        if f["id"] == faculty_id:
            faculty[i] = updated.dict()
            save_faculty()
            return updated
    raise HTTPException(status_code=404, detail="Faculty not found")

@router.delete("/{faculty_id}", status_code=204)
def delete_faculty(faculty_id: int):
    global faculty
    initial_len = len(faculty)
    faculty = [f for f in faculty if f["id"] != faculty_id]
    if len(faculty) == initial_len:
        raise HTTPException(status_code=404, detail="Faculty not found")
    save_faculty()
    return

@router.get("/faculty/{faculty_id}/courses")
def courses_by_faculty(faculty_id: int):
    return [c for c in courses if c["faculty_id"] == faculty_id]

@router.get("/faculty/most-courses")
def faculty_most_courses():
    faculty_course_count = {f["id"]: 0 for f in faculty}
    for c in courses:
        fid = c["faculty_id"]
        if fid in faculty_course_count:
            faculty_course_count[fid] += 1
    max_courses = max(faculty_course_count.values())
    top_faculty = [f for f in faculty if faculty_course_count[f["id"]] == max_courses]
    return {"max_courses": max_courses, "faculty": top_faculty}

@router.get("/faculty/availability")
def faculty_availability(day: str, start: str, end: str):
    return [f for f in faculty if day.lower() in f["office_hours"].lower()]

@router.get("/faculty/contact-list/{department}")
def faculty_contact_list(department: str):
    return [{
        "name": f"{f['first_name']} {f['last_name']}",
        "email": f["email"],
        "office_location": f["office_location"]
    } for f in faculty if f["department"].lower() == department.lower()]

@router.patch("/{faculty_id}")
def update_faculty_partial(faculty_id: int, updates: dict = Body(...)):
    prof = next((f for f in faculty if f["id"] == faculty_id), None)
    if not prof:
        raise HTTPException(404, "Faculty not found")
    for key, value in updates.items():
        if key in prof:
            prof[key] = value
    save_faculty()
    return prof

@router.get("/search")
def search_faculty(query: str = Query(..., description="Search across all faculty fields")):
    q = query.lower()
    result = []
    for f in faculty:
        if (
            q in str(f.get("id", "")).lower()
            or q in f.get("first_name", "").lower()
            or q in f.get("last_name", "").lower()
            or q in f.get("email", "").lower()
            or q in f.get("department", "").lower()
            or q in f.get("office_location", "").lower()
            or q in f.get("office_hours", "").lower()
            or any(q in s.lower() for s in f.get("specialization", []))
        ):
            result.append(f)
    return result

@router.get("/faculty/fuzzy")
def fuzzy_faculty_search(term: str, threshold: int = 80):
    names = [f"{f['first_name']} {f['last_name']}" for f in faculty]
    matches = get_close_matches(term, names, cutoff=threshold / 100.0)
    return [
        f for f in faculty if f"{f['first_name']} {f['last_name']}" in matches
    ]

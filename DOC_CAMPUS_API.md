
# 📘 College Campus API

A RESTful API for managing, searching, and analyzing college course and faculty data.

## ⚙️ Setup Instructions

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Go to main.py 's file:**

   ```bash
   cd app
   ```

3. **Run the API server:**

   ```bash
   python -m uvicorn main:app --reload
   ```

4. Access the API via:

   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
   - Root HTML: [http://localhost:8000/](http://localhost:8000/)

## 📚 Data Models

### Course

```python
class Course(BaseModel):
    id: int
    name: str
    code: str
    description: str
    credits: int
    department: str
    prerequisites: List[int]
    faculty_id: int
```

### Faculty

```python
class Faculty(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    specialization: List[str]
    office_location: str
    office_hours: str
```

## 🧭 Endpoint Reference

### 📂 `/courses`

| Method | Endpoint                      | Description                                  |
|--------|-------------------------------|----------------------------------------------|
| GET    | `/courses`                    | Get all courses, with pagination & sorting   |
| GET    | `/courses/search`            | Search across all course fields              |
| GET    | `/courses/{course_id}`        | Get single course by ID                      |
| POST   | `/courses`                    | Create new course                            |
| PUT    | `/courses/{course_id}`        | Update full course                           |
| PATCH  | `/courses/{course_id}`        | Partial update                               |
| DELETE | `/courses/{course_id}`        | Delete course                                |

#### 📊 Analytics & Search

| Endpoint | Description |
|----------|-------------|
| `/courses/{course_id}/prerequisites/full` | Full prerequisite chain with faculty info |
| `/courses/{course_id}/prerequisite-path` | Recursive prerequisite lineage |
| `/courses/no-prerequisites`              | Courses without prerequisites |
| `/courses/most-prerequisites`           | Top N courses with most prerequisites |
| `/courses/by-semester/{semester}`       | Courses offered in a semester |
| `/courses/specialization`               | Courses matching faculty specialization |
| `/courses/match-interest`               | Courses based on field interest |
| `/courses/recommend`                    | Auto-recommend courses based on topics |
| `/courses/fuzzy`                        | Fuzzy search course names |

### 👨‍🏫 `/faculty`

| Method | Endpoint                      | Description                       |
|--------|-------------------------------|-----------------------------------|
| GET    | `/faculty`                    | Get all faculty                   |
| GET    | `/faculty/{faculty_id}`       | Get faculty by ID                 |
| POST   | `/faculty`                    | Add new faculty                   |
| PUT    | `/faculty/{faculty_id}`       | Update full faculty record        |
| PATCH  | `/faculty/{faculty_id}`       | Partial update                    |
| DELETE | `/faculty/{faculty_id}`       | Delete faculty                    |

#### Additional Faculty Endpoints

| Endpoint                               | Description                                     |
|----------------------------------------|-------------------------------------------------|
| `/faculty/search`                      | General search by name, specialty, etc.         |
| `/faculty/fuzzy`                       | Fuzzy search by name                            |
| `/faculty/faculty/{faculty_id}/courses` | Courses taught by a faculty member              |
| `/faculty/most-courses`                | Faculty with most courses                       |
| `/faculty/availability`                | Filter by availability range                    |
| `/faculty/contact-list/{department}`   | Quick access to department contact info         |

### 🧠 `/advanced`

| Endpoint                             | Description                                      |
|--------------------------------------|--------------------------------------------------|
| `/advanced/courses/by-credits`       | Filter courses by minimum credit threshold       |
| `/advanced/faculty/available-on`     | Faculty available on a certain day               |
| `/advanced/courses/search`           | Search courses by name or description            |
| `/advanced/analytics/faculty-course-load` | Faculty with heaviest teaching load        |
| `/advanced/faculty/specialization`   | Match specialization by topic                    |
| `/advanced/courses/with-faculty`     | Courses enriched with faculty details            |
| `/advanced/search/all`               | Search across both courses and faculty           |
| `/advanced/departments/course-count` | Number of courses offered by each department     |

## ✅ Notes

- All endpoints follow REST conventions.
- Path parameters like `{course_id}` and `{faculty_id}` are required and must be integers.
- Complex search and filtering use query parameters (e.g., `?query=data` or `?topics=ai`).
- Data is stored in JSON files (`courses.json`, `faculty.json`) and changes are saved automatically.


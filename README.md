# 🎓 College Campus API

A FastAPI-powered REST API for managing and analyzing college course and faculty data, complete with smart search, analytics, and auto-generated documentation.

## 🚀 Features

- **Full CRUD** for courses and faculty via clean RESTful endpoints
- **Advanced search**: Fuzzy matching, field-based queries
- **Analytics**: Faculty workloads, department stats, recommendations
- **Auto documentation**: Interactive Swagger UI (`/docs`) and ReDoc (`/redoc`)
- **Validation**: Enforces correct input types using Pydantic models
- **Easy integration**: Consumes and returns JSON

## 📦 Project Structure

| File            | Purpose                                      |
|-----------------|----------------------------------------------|
| `main.py`       | API entrypoint and router setup              |
| `courses.py`    | Course management endpoints                  |
| `faculty.py`    | Faculty management endpoints                 |
| `advanced.py`   | Analytics, special searches, recommendations |
| `models.py`     | Pydantic schemas for validation              |
| `database.py`   | JSON data I/O utilities                      |
| `requirements.txt` | Python dependencies                       |
| `mock_data/*.json` | Sample course and faculty data (optional)  |

## ⚙️ Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
2. **Go to main.py 's folder**
    ```bash
   cd app
   ```
    
3. **Run the API server:**
   ```bash
   uvicorn main:app --reload
   ```
   
4. **Access API documentation:**
   - [Swagger UI](http://localhost:8000/docs)
   - [ReDoc](http://localhost:8000/redoc)

## 🛠️ Usage Examples

**Get all courses:**
```bash
curl http://localhost:8000/courses
```

**Add a new faculty member:**
```bash
curl -X POST http://localhost:8000/faculty \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Alice", "last_name": "Wong", "email": "alice@campus.edu", ...}'
```

**Search faculty by specialization:**
```bash
curl "http://localhost:8000/advanced/faculty/specialization/?topic=data%20science"
```

See `/docs` for all endpoints and input examples.

## 📝 Data Models

**Course:**
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

**Faculty:**
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

## 🏁 Key Endpoints

| Method | Endpoint                       | Purpose                                   |
|--------|------------------------------- |-------------------------------------------|
| GET    | `/courses`                     | List all courses, search, filter, sort    |
| GET    | `/courses/{course_id}`         | Get details of a single course            |
| POST   | `/courses`                     | Add a new course                          |
| PUT    | `/courses/{course_id}`         | Full course update                        |
| PATCH  | `/courses/{course_id}`         | Partial course update                     |
| DELETE | `/courses/{course_id}`         | Remove a course                           |
| GET    | `/faculty`                     | List all faculty, search, filter          |
| ...    | ...                            | See `/docs` for full reference            |
| GET    | `/advanced/*`                  | Analytics, fuzzy search, matching         |

## ✅ Validation & Error Handling

- All endpoints enforce strict type checking.
- If input data is missing or has the wrong type, API returns `422 Unprocessable Entity` with details for fast debugging.

## 🌱 Future Scope

- Integrate with a production database (PostgreSQL/MySQL)
- Add authentication and role-based access
- Expand endpoints to support student records, enrollment, and grading
- Build a React or Vue front-end portal

## 🙏 Contributing

1. Fork the repo & create a new branch
2. Add/edit features or fix bugs
3. Make sure all code passes type checks/tests

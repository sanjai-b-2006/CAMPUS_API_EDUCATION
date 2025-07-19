from pydantic import BaseModel
from typing import List

class Faculty(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    department: str
    specialization: List[str]
    office_location: str
    office_hours: str

class Course(BaseModel):
    id: int
    name: str
    code: str
    description: str
    credits: int
    department: str
    prerequisites: List[int]
    faculty_id: int

from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List
from datetime import date
from enum import Enum

class LectureType(str, Enum):
    LECTURE = 'lecture'
    QUIZ = 'quiz'
    CODING_EXERCISE = 'coding_exercise'
    ARTICLE = 'article'

class CourseUrlInput(BaseModel):
    url: HttpUrl

class ScheduleInput(BaseModel):
    course_id: str
    days_until_completion: Optional[int] = None
    hours_per_day: Optional[int] = None
    start_date: Optional[date] = None
    pausing_buffer: bool = False
    video_speed: float = 1.0

class LectureResponse(BaseModel):
    id: int
    title: str
    lecture_type: LectureType
    duration_seconds: int

class CourseResponse(BaseModel):
    id: str
    title: str
    total_duration_seconds: int
    sections_and_lectures: Dict[str, List[LectureResponse]]

class ScheduleResponse(BaseModel):
    course_title: str
    total_duration: str
    schedule: Dict[str, List[LectureResponse]]
    completion_info: str 
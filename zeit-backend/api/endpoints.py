from fastapi import APIRouter, HTTPException
from models.schemas import CourseUrlInput, ScheduleInput, CourseResponse, ScheduleResponse
from services.course_builder import CourseBuilder
from services.schedule_maker import ScheduleMaker

router = APIRouter()
course_builder = CourseBuilder()
schedule_maker = ScheduleMaker()

@router.post("/courses/validate")
async def validate_course_url(course_input: CourseUrlInput):
    is_valid_id, is_valid_link = await course_builder.validate_url(str(course_input.url))
    return {"is_valid": is_valid_id or is_valid_link}

@router.post("/courses/details", response_model=CourseResponse)
async def get_course_details(course_input: CourseUrlInput):
    try:
        return await course_builder.get_course_details(str(course_input.url))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch course details")

@router.post("/courses/schedule", response_model=ScheduleResponse)
async def create_schedule(schedule_input: ScheduleInput):
    try:
        # First get course details
        course_url = f"https://www.udemy.com/course-dashboard-redirect/?course_id={schedule_input.course_id}"
        course_details = await course_builder.get_course_details(course_url)
        
        # Then create schedule
        return await schedule_maker.create_schedule(course_details, schedule_input)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create schedule") 
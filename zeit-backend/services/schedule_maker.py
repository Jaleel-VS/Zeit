from datetime import date, timedelta
from typing import Dict, List
from models.schemas import CourseResponse, LectureResponse, ScheduleInput, ScheduleResponse

PAUSING_BUFFER_RATIO = 1.5

class ScheduleMaker:
    def __init__(self):
        pass

    async def create_schedule(self, course: CourseResponse, schedule_input: ScheduleInput) -> ScheduleResponse:
        if schedule_input.days_until_completion:
            schedule = await self._build_by_days(course, schedule_input)
        else:
            schedule = await self._build_by_hours(course, schedule_input)
            
        completion_info = await self._generate_completion_info(course, schedule_input)
        
        return ScheduleResponse(
            course_title=course.title,
            total_duration=f"{course.total_duration_seconds // 3600}:{course.total_duration_seconds % 3600 // 60:02}",
            schedule=schedule,
            completion_info=completion_info
        )

    async def _build_by_days(self, course: CourseResponse, schedule_input: ScheduleInput) -> Dict[str, List[LectureResponse]]:
        seconds_per_day = await self._calculate_seconds_per_day(
            course.total_duration_seconds,
            schedule_input.days_until_completion,
            schedule_input.video_speed,
            schedule_input.pausing_buffer
        )
        
        return await self._distribute_lectures(
            course.sections_and_lectures,
            seconds_per_day,
            schedule_input.start_date or date.today() + timedelta(days=1),
            schedule_input.video_speed,
            schedule_input.pausing_buffer
        )

    async def _build_by_hours(self, course: CourseResponse, schedule_input: ScheduleInput) -> Dict[str, List[LectureResponse]]:
        seconds_per_day = schedule_input.hours_per_day * 3600
        
        return await self._distribute_lectures(
            course.sections_and_lectures,
            seconds_per_day,
            schedule_input.start_date or date.today() + timedelta(days=1),
            schedule_input.video_speed,
            schedule_input.pausing_buffer
        )

    async def _calculate_seconds_per_day(self, total_seconds: int, days: int, video_speed: float, pausing_buffer: bool) -> float:
        base_seconds = total_seconds / days / video_speed
        return base_seconds * PAUSING_BUFFER_RATIO if pausing_buffer else base_seconds

    async def _distribute_lectures(
        self,
        sections_and_lectures: Dict[str, List[LectureResponse]],
        seconds_per_day: float,
        start_date: date,
        video_speed: float,
        pausing_buffer: bool
    ) -> Dict[str, List[LectureResponse]]:
        lectures_per_day = {}
        current_day = 1
        current_date = start_date
        cumulative_seconds = 0
        
        day_key = f"Day {current_day} ({current_date.strftime('%Y-%m-%d')})"
        lectures_per_day[day_key] = []

        for section_lectures in sections_and_lectures.values():
            for lecture in section_lectures:
                duration = lecture.duration_seconds
                if pausing_buffer:
                    duration *= PAUSING_BUFFER_RATIO
                duration /= video_speed
                
                cumulative_seconds += duration
                lectures_per_day[day_key].append(lecture)

                if cumulative_seconds >= seconds_per_day:
                    cumulative_seconds = 0
                    current_day += 1
                    current_date += timedelta(days=1)
                    day_key = f"Day {current_day} ({current_date.strftime('%Y-%m-%d')})"
                    lectures_per_day[day_key] = []

        return lectures_per_day

    async def _generate_completion_info(self, course: CourseResponse, schedule_input: ScheduleInput) -> str:
        if schedule_input.days_until_completion:
            hours_per_day = course.total_duration_seconds / schedule_input.days_until_completion / 3600
            if schedule_input.pausing_buffer:
                hours_per_day *= PAUSING_BUFFER_RATIO
            return f"To complete the course in {schedule_input.days_until_completion} days, you will need to spend about {round(hours_per_day, 2)} hours per day."
        else:
            return f"If you spend {schedule_input.hours_per_day} hours per day, you will complete the course in {course.total_duration_seconds // (schedule_input.hours_per_day * 3600) + 1} days." 
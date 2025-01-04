from typing import Dict, List, Tuple
import requests
import re
from models.schemas import LectureType, LectureResponse, CourseResponse

QUIZ_QUESTION_LENGTH = 2  # in minutes
CODING_EXERCISE_LENGTH = 5  # in minutes

lecture_identifier = {
    "udi udi-video": LectureType.LECTURE,
    "udi udi-article": LectureType.ARTICLE,
    "udi udi-quiz": LectureType.QUIZ,
    "udi udi-coding-exercise": LectureType.CODING_EXERCISE
}

class CourseBuilder:
    def __init__(self):
        self.CURRICULUM_ENDPOINT = "https://www.udemy.com/api-2.0/course-landing-components/{}/me/?components=curriculum_context"

    async def validate_url(self, url: str) -> Tuple[bool, bool]:
        pattern_with_id = r'https://www.udemy.com/course-dashboard-redirect/\?course_id=\d+'
        pattern_with_course_link = r'https://www.udemy.com/course/[^/]+/'
        return bool(re.match(pattern_with_id, str(url))), bool(re.match(pattern_with_course_link, str(url)))

    async def get_course_details(self, url: str) -> CourseResponse:
        is_valid_id, is_valid_link = await self.validate_url(url)
        
        if not (is_valid_id or is_valid_link):
            raise ValueError("Invalid URL format")

        try:
            course_id, course_title = await self._extract_course_info(url, is_valid_id)
            course_detail = await self._fetch_curriculum(course_id)
            return await self._build_course_response(course_id, course_title, course_detail)
        except Exception as e:
            raise ValueError(f"Failed to fetch course details: {str(e)}")

    async def _extract_course_info(self, url: str, is_id_format: bool) -> Tuple[str, str]:
        if is_id_format:
            course_id = url.split("=")[1]
            endpoint_url = f"https://www.udemy.com/api-2.0/courses/{course_id}/?fields[course]=title"
            response = requests.get(endpoint_url)
            response.raise_for_status()
            return course_id, response.json()['title']
        else:
            response = requests.get(url)
            pattern_id = r'/(\d+)_'
            pattern_title = r'<meta name="title" content="([^"]+)">'
            course_id = re.search(pattern_id, response.text).group(1)
            course_title = re.search(pattern_title, response.text).group(1)
            return course_id, course_title

    async def _fetch_curriculum(self, course_id: str) -> Dict:
        endpoint_url = self.CURRICULUM_ENDPOINT.format(course_id)
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()
        return data['curriculum_context']['data']['sections']

    async def _build_course_response(self, course_id: str, course_title: str, sections: List) -> CourseResponse:
        sections_and_lectures = {}
        total_duration_seconds = 0

        for section in sections:
            lectures = []
            for lecture in section['items']:
                lecture_type = lecture_identifier[lecture['icon_class']]
                duration = await self._calculate_duration(lecture['content_summary'], lecture_type)
                
                lecture_response = LectureResponse(
                    id=lecture['id'],
                    title=lecture['title'],
                    lecture_type=lecture_type,
                    duration_seconds=duration
                )
                lectures.append(lecture_response)
                total_duration_seconds += duration
            
            sections_and_lectures[section['title']] = lectures

        return CourseResponse(
            id=course_id,
            title=course_title,
            total_duration_seconds=total_duration_seconds,
            sections_and_lectures=sections_and_lectures
        )

    async def _calculate_duration(self, content_summary: str, lecture_type: LectureType) -> int:
        if lecture_type in [LectureType.LECTURE, LectureType.ARTICLE]:
            pattern = r'(\d+):(\d+)'
            match = re.search(pattern, content_summary)
            if match:
                return int(match.group(1)) * 60 + int(match.group(2))
        elif lecture_type in [LectureType.QUIZ, LectureType.CODING_EXERCISE]:
            pattern = r'(\d+) question'
            match = re.search(pattern, content_summary)
            if match:
                questions = int(match.group(1))
                return questions * (QUIZ_QUESTION_LENGTH if lecture_type == LectureType.QUIZ else CODING_EXERCISE_LENGTH) * 60
        return 0 
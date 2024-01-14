from enum import Enum
import re

QUIZ_QUESTION_LENGTH = 2 # in minutes
CODING_EXERCISE_LENGTH = 5 # in minutes

class LectureType(Enum):
    LECTURE = 'lecture'
    QUIZ = 'quiz'
    CODING_EXERCISE = 'coding_exercise'
    ARTICLE = 'article'

lecture_identifier = {
    "udi udi-video": LectureType.LECTURE,
    "udi udi-article": LectureType.ARTICLE,
    "udi udi-quiz": LectureType.QUIZ,
    "udi udi-coding-exercise": LectureType.CODING_EXERCISE
}


def get_question_count(question_text: str) -> int:
    """ Parse the number of questions from a string and return the count. """
    pattern = r'(\d+) question'
    match = re.search(pattern, question_text)
    if match:
        return int(match.group(1))
    else:
        return 0

    
def parse_duration(duration: str, pattern: str) -> (int, int):
    """ Parse duration using the provided pattern and return both minutes and seconds. """
    match = re.search(pattern, duration)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        return 0, 0

def get_lecture_duration_seconds(duration: str, lecture_type: LectureType) -> int:
    """ Calculate the lecture duration in seconds based on its type. """
    # Patterns for matching duration
    pattern_duration = r'(\d+):(\d+)'
    pattern_quiz_question = r'(\d+) question'

    if lecture_type in (LectureType.LECTURE, LectureType.ARTICLE):
        minutes, seconds = parse_duration(duration, pattern_duration)
        return minutes * 60 + seconds

    elif lecture_type in (LectureType.QUIZ, LectureType.CODING_EXERCISE):
        question_count = get_question_count(duration)
        if lecture_type == LectureType.QUIZ:
            return question_count * QUIZ_QUESTION_LENGTH * 60
        else:  # LectureType.CODING_EXERCISE
            return question_count * CODING_EXERCISE_LENGTH * 60

    return 0  # Default return if none of the types match

    
class Lecture:
    def __init__(self, id: int, title: str, lecture_type: LectureType, duration_seconds: int):
        self.id = id
        self.title = title
        self.lecture_type = lecture_type
        self.duration_seconds = duration_seconds

class CourseBuilder:
    def __init__(self, id, title, course_detail):
        self._raw_course_detail = course_detail
        self.id = id
        self.title = title
        self.sections_and_lectures: dict[str, list[Lecture]] = {}
        self.total_duration_seconds = 0

    def build(self):
        for section in self._raw_course_detail:
            section_name = section
            lectures = []
            for lecture in self._raw_course_detail[section]:
                lecture_id = lecture["id"]
                lecture_title = lecture["title"]
                lecture_icon = lecture["icon_class"]
                lecture_type = lecture_identifier[lecture_icon]
                lecture_duration_seconds = get_lecture_duration_seconds(lecture["content_summary"], lecture_type)
                lectures.append(Lecture(lecture_id, lecture_title, lecture_type, lecture_duration_seconds))
                self.total_duration_seconds += lecture_duration_seconds
            self.sections_and_lectures[section_name] = lectures

    def export_to_txt(self):
        with open(f"{self.title}.txt", "w") as file:
            file.write(f"{self.title}\n")
            for section in self.sections_and_lectures:
                file.write(f"\n{section}\n")
                file.write("*-" * 20 + "\n")
                for lecture in self.sections_and_lectures[section]:
                    # title - duration (mm:ss) (lecture type)
                    file.write(f"{lecture.title} - {lecture.duration_seconds // 60}:{lecture.duration_seconds % 60:02} ({lecture.lecture_type.value})\n")
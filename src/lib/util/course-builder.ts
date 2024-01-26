enum LectureType {
    LECTURE = 'lecture',
    QUIZ = 'quiz',
    CODING_EXERCISE = 'coding_exercise',
    ARTICLE = 'article',
}

const QUIZ_QUESTION_LENGTH = 2; // in minutes
const CODING_EXERCISE_LENGTH = 5; // in minutes

const lectureIdentifier: { [key: string]: LectureType } = {
    "udi udi-video": LectureType.LECTURE,
    "udi udi-article": LectureType.ARTICLE,
    "udi udi-quiz": LectureType.QUIZ,
    "udi udi-coding-exercise": LectureType.CODING_EXERCISE,
};

function getQuestionCount(questionText: string): number {
    const pattern = /(\d+) question/;
    const match = questionText.match(pattern);
    return match ? parseInt(match[1]) : 0;
}

function parseDuration(duration: string, pattern: string): [number, number] {
    const match = duration.match(pattern);
    return match ? [parseInt(match[1]), parseInt(match[2])] : [0, 0];
}

function getLectureDurationSeconds(duration: string, lectureType: LectureType): number {
    const patternDuration = "(\d+):(\d+)"; // Updated to a string pattern

    if (lectureType === LectureType.LECTURE || lectureType === LectureType.ARTICLE) {
        const [minutes, seconds] = parseDuration(duration, patternDuration);
        return minutes * 60 + seconds;
    } else if (lectureType === LectureType.QUIZ || lectureType === LectureType.CODING_EXERCISE) {
        const questionCount = getQuestionCount(duration);
        return lectureType === LectureType.QUIZ
            ? questionCount * QUIZ_QUESTION_LENGTH * 60
            : questionCount * CODING_EXERCISE_LENGTH * 60;
    }

    return 0;
}

export class Lecture {
    id: number;
    title: string;
    lectureType: LectureType;
    durationSeconds: number;

    constructor(id: number, title: string, lectureType: LectureType, durationSeconds: number) {
        this.id = id;
        this.title = title;
        this.lectureType = lectureType;
        this.durationSeconds = durationSeconds;
    }
}

export class CourseBuilder {
    rawCourseDetail: any;
    id: number;
    title: string;
    sectionsAndLectures: Record<string, Lecture[]>;
    totalDurationSeconds: number;

    constructor(id: number, title: string, courseDetail: any) {
        this.rawCourseDetail = courseDetail;
        this.id = id;
        this.title = title;
        this.sectionsAndLectures = {};
        this.totalDurationSeconds = 0;
    }

    build(): void {
        for (const section in this.rawCourseDetail) {
            const lectures: Lecture[] = [];
            for (const lectureData of this.rawCourseDetail[section]) {
                const lectureType = lectureIdentifier[lectureData.icon_class];
                const lectureDurationSeconds = getLectureDurationSeconds(lectureData.content_summary, lectureType);
                lectures.push(new Lecture(lectureData.id, lectureData.title, lectureType, lectureDurationSeconds));
                this.totalDurationSeconds += lectureDurationSeconds;
            }
            this.sectionsAndLectures[section] = lectures;
        }
    }


}

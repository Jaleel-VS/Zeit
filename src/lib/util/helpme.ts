import * as fs from 'fs';

// const fs 

const QUIZ_QUESTION_LENGTH = 2 // minutes, time to answer a question
const CODING_EXERCISE_LENGTH = 5
const PAUSING_BUFFER_RATIO = 1.5 // eg a 10 minute lecture will be scheduled for 15 minutes



enum LectureType {
    LECTURE = 'lecture',
    QUIZ = 'quiz',
    CODING_EXERCISE = 'coding exercise',
    ARTICLE = 'article',
}




interface Lecture {
    id: string;
    type: LectureType;
    title: string;
    durationSeconds: number;
    section: string;
}




const getQuesionCount = (questionText: string): number => {
    const pattern = /(\d+) questions/;

    const match = questionText.match(pattern);

    if (match === null) {
        return 0;
    }

    return parseInt(match[1]);
}

const parseDuration = (duration: string, pattern: RegExp): [number, number] => {
    console.log(`duration: ${duration}`);
    const match = duration.match(pattern);

    if (match === null) {
        return [0, 0];
    }

    const minutes = parseInt(match[1]);
    const seconds = parseInt(match[2]);

    return [minutes, seconds];
}

const getLectureDurationInSeconds = (duration: string, lectureType: LectureType): number => {
    const durationPattern = /(\d+):(\d+)/;

    if (lectureType === LectureType.LECTURE || lectureType === LectureType.ARTICLE) {
        const _duration = parseDuration(duration, durationPattern);
        return _duration[0] * 60 + _duration[1];
    }

    else if (lectureType === LectureType.QUIZ || lectureType === LectureType.CODING_EXERCISE) {
        const questionCount = getQuesionCount(duration);

        if (lectureType === LectureType.QUIZ) {
            return questionCount * QUIZ_QUESTION_LENGTH * 60;
        } else {
            return questionCount * CODING_EXERCISE_LENGTH * 60;
        }
    }

    return 0;
}



interface ScheduleOptions {
    hoursPerDay: number;
    daysUntilCompletion: number;
    startDate: Date;
    pausingBuffer: boolean;
    videoSpeed: number;
}

const createScheduleOptions = (hoursPerDay: number, daysUntilCompletion: number, startDate: Date, pausingBuffer: boolean, videoSpeed: number): ScheduleOptions => {
    return {
        hoursPerDay,
        daysUntilCompletion,
        startDate,
        pausingBuffer,
        videoSpeed,
    }
}

interface Item {
    id: string,
    title: string,
    content_summary: string,
    icon_class: string
}

interface Section {
    index: number;
    title: string;
    items: Item[];
}

const getLectureType = (text: string): LectureType => {

    const pattern = /udi udi-(\w+)/;

    const match = text.match(pattern);

    if (match === null) {
        return LectureType.LECTURE;
    }

    const type = match[1];

    if (type === 'video') {
        return LectureType.LECTURE;
    } else if (type === 'article') {
        return LectureType.ARTICLE;
    } else if (type === 'quiz') {
        return LectureType.QUIZ;
    } else if (type === 'coding-exercise') {
        return LectureType.CODING_EXERCISE;
    } else {
        return LectureType.LECTURE;
    }

}


const createLectures = (data: { sections: Section[] }): Lecture[] => {
    const lectures: Lecture[] = [];

    data.sections.forEach((section) => {
        section.items.forEach((item) => {
            const type = getLectureType(item.icon_class);
            const lecture: Lecture = {
                id: item.id,
                type: type,
                title: item.title,
                durationSeconds: getLectureDurationInSeconds(item.content_summary, type),
                section: section.title,
            };

            lectures.push(lecture);
        });
    });

    return lectures;
}


const buildSchedule = (lectures: Lecture[], options: ScheduleOptions): Record<string, Lecture[]> => {
    if (options.hoursPerDay > 0) {
        return buildScheduleWithHoursPerDay(lectures, options);
    }

    return buildScheduleWithDaysUntilCompletion(lectures, options);

}

const buildScheduleWithHoursPerDay = (lectures: Lecture[], options: ScheduleOptions): Record<string, Lecture[]> => {
    const secondsPerDay = options.hoursPerDay * 60 * 60;
    const lecturesPerDay: Record<string, Lecture[]> = {};
    let currentDay = 1;
    const date = options.startDate;
    let cummalativeSeconds = 0;
    const formatDay = (day: number, date: Date): string => {
        return `Day ${day} (${date.toDateString()})`;
    }
    lecturesPerDay[formatDay(currentDay, date)] = [];

    lectures.forEach((lecture) => {
        let lectureDuration = lecture.durationSeconds / options.videoSpeed;
        if (options.pausingBuffer) {
            lectureDuration *= PAUSING_BUFFER_RATIO;
        }

        cummalativeSeconds += lectureDuration;

        if (cummalativeSeconds > secondsPerDay) {
            currentDay += 1;
            date.setDate(date.getDate() + 1);
            cummalativeSeconds = 0;
            lecturesPerDay[formatDay(currentDay, date)] = [];
        }

        lecturesPerDay[formatDay(currentDay, date)].push(lecture);

    });

    return lecturesPerDay;
}

const buildScheduleWithDaysUntilCompletion = (lectures: Lecture[], options: ScheduleOptions): Record<string, Lecture[]> => {
    const totalSeconds = lectures.reduce((acc, lecture) => {
        return acc + lecture.durationSeconds;
    }, 0);

    const secondsPerDay = totalSeconds / options.daysUntilCompletion;

    const lecturesPerDay: Record<string, Lecture[]> = {};
    let currentDay = 1;
    const date = options.startDate;
    let cummalativeSeconds = 0;
    const formatDay = (day: number, date: Date): string => {
        return `Day ${day} (${date.toDateString()})`;
    }
    lecturesPerDay[formatDay(currentDay, date)] = [];

    lectures.forEach((lecture) => {
        let lectureDuration = lecture.durationSeconds / options.videoSpeed;
        if (options.pausingBuffer) {
            lectureDuration *= PAUSING_BUFFER_RATIO;
        }

        cummalativeSeconds += lectureDuration;

        if (cummalativeSeconds > secondsPerDay) {
            currentDay += 1;
            date.setDate(date.getDate() + 1);
            cummalativeSeconds = 0;
            lecturesPerDay[formatDay(currentDay, date)] = [];
        }

        lecturesPerDay[formatDay(currentDay, date)].push(lecture);

    });

    return lecturesPerDay;
}

const getData = async (): Promise<{ sections: Section[] }> => {
    const filePath = './dummy.json';

    const fileContent = fs.readFileSync(filePath, 'utf8');

    const data = JSON.parse(fileContent);

    return data;
}
export const getSchedule = async (
    hoursPerDay: number,
    daysUntilCompletion: number,
    startDate: Date,
    pausingBuffer: boolean,
    videoSpeed: number,

) => {
    const data = await getData();
    const lectures = createLectures(data);
    const options = createScheduleOptions(0, 7, new Date(), true, 1);
    const schedule = buildSchedule(lectures, options);

    if (schedule) {
        console.log("Schedule created successfully");
    }

    else {
        console.log("Failed to create schedule");
    }
}

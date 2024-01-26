import { CourseBuilder, Lecture } from "./course-builder";

const PAUSING_BUFFER_RATIO = 1.5; // a 1 hour lecture will take 1.5 hours to complete with the pausing buffer

export class Schedule {
    private course: CourseBuilder;
    private daysUntilCompletion: number;
    private hoursPerDay: number;
    private startDate: Date | null;
    private pausingBuffer: boolean;
    private videoSpeed: number;
    private lecturesPerDay: Record<string, Lecture[]>;

    constructor(course: CourseBuilder) {
        this.course = course;
        this.daysUntilCompletion = -1;
        this.hoursPerDay = -1;
        this.startDate = null;
        this.pausingBuffer = false;
        this.videoSpeed = 1.0;
        this.lecturesPerDay = {};
    }

    build(): void {
        if (this.daysUntilCompletion !== -1) {
            this.buildByDays();
        } else {
            this.buildByHours();
        }
    }

    private buildByDays(): void {
        const lecturesPerSection = this.course.sectionsAndLectures;
        const secondsPerDay = (this.course.totalDurationSeconds / this.daysUntilCompletion / this.videoSpeed) * (this.pausingBuffer ? PAUSING_BUFFER_RATIO : 1);

        let currentDay = 1;
        let date = new Date(this.startDate!);

        let cumulativeSeconds = 0;
        for (const section in lecturesPerSection) {
            for (const lecture of lecturesPerSection[section]) {
                let lectureDuration = lecture.durationSeconds;
                if (this.pausingBuffer) {
                    lectureDuration *= PAUSING_BUFFER_RATIO;
                }
                cumulativeSeconds += lectureDuration / this.videoSpeed;

                const formattedDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
                const dayKey = `Day ${currentDay} (${formattedDate})`;
                this.lecturesPerDay[dayKey] = this.lecturesPerDay[dayKey] || [];
                this.lecturesPerDay[dayKey].push(lecture);

                if (cumulativeSeconds >= secondsPerDay) {
                    cumulativeSeconds = 0;
                    currentDay++;
                    date.setDate(date.getDate() + 1);
                }
            }
        }

    }

    private buildByHours(): void {
        const lecturesPerSection = this.course.sectionsAndLectures;
        const secondsPerDay = this.hoursPerDay * 3600; // Convert hours to seconds
        let currentDay = 1;
        let date = new Date(this.startDate!);
    
        let cumulativeSeconds = 0;
        for (const section in lecturesPerSection) {
            for (const lecture of lecturesPerSection[section]) {
                let lectureDuration = lecture.durationSeconds;
                if (this.pausingBuffer) {
                    lectureDuration *= PAUSING_BUFFER_RATIO;
                }
                cumulativeSeconds += lectureDuration / this.videoSpeed;
    
                const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
                const dayKey = `Day ${currentDay} (${formattedDate})`;
                this.lecturesPerDay[dayKey] = this.lecturesPerDay[dayKey] || [];
                this.lecturesPerDay[dayKey].push(lecture);
    
                if (cumulativeSeconds >= secondsPerDay) {
                    cumulativeSeconds = 0;
                    currentDay++;
                    date.setDate(date.getDate() + 1);
                }
            }
        }
    }


    
    

    
}


import { getCourseDetails } from '$lib/util/course-details';
import { getLectures } from '$lib/util/schedule-helper';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    const getCourseIdAndTitle = async(websiteURL: string) => {
        console.log("Obteniendo detalles del curso...");
        const courseDetails = await getCourseDetails(websiteURL);
        console.log(courseDetails);
        const courseID = courseDetails['courseId'];
        const courseName = courseDetails['courseTitle'];

        let lectures = {};

        if (courseID) {
            lectures = await getLectures(courseID);
        }
        return { 
            lectures: lectures,
        };
    }
    return {
        courseDetails: getCourseIdAndTitle("udemy.com/course-dashboard-redirect/?course_id=1026604")};
}) satisfies PageServerLoad;
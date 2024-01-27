import { getCourseDetails } from '$lib/util/course-details';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    const getCourseIdAndTitle = async (websiteURL: string) => {
        console.log("Obteniendo detalles del curso...");
        const courseDetails = await getCourseDetails(websiteURL);
        console.log(courseDetails);
        const courseID = courseDetails['courseId'];
        const courseName = courseDetails['courseTitle'];

        return {
            courseID,
            courseName
        };
    }
    return {
        courseDetails: getCourseIdAndTitle("udemy.com/course-dashboard-redirect/?course_id=102664")
    };
}) satisfies PageServerLoad;
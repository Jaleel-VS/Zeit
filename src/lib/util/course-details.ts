import fetch from 'node-fetch';

export async function getCourseDetails(websiteUrl: string) {
    console.log("Function getCourseDetails called");
    const websiteText = await getWebsiteText(websiteUrl);
    if (!websiteText) {
        return { courseId: null, courseTitle: null };
    }
    return extractCourseIdAndTitle(websiteText);
}

function extractCourseIdAndTitle(websiteText: string) {
    const patternId = /\/(\d+)_/;
    const patternTitle = /<meta name="title" content="([^"]+)">/;
    const courseId = websiteText.match(patternId)?.[1] ?? null;
    const courseTitle = websiteText.match(patternTitle)?.[1] ?? null;
    return { courseId, courseTitle };
}

export function isValidUrl(websiteUrl: string): boolean {
    websiteUrl = websiteUrl.toLowerCase();
    if (!websiteUrl.includes("udemy")) {
        console.error("URL is not from Udemy");
        return false;
    }


    const patternWithId = /udemy\.com\/course-dashboard-redirect\/\?course_id=\d+\/?$/;
    const patternWithCourseLink = /udemy\.com\/course\/[^/]+\/?/;
    return patternWithId.test(websiteUrl) || patternWithCourseLink.test(websiteUrl);
}

async function getWebsiteText(websiteUrl: string): Promise<string | null> {
    // Add protocol if missing
    if (!websiteUrl.startsWith('http://') && !websiteUrl.startsWith('https://')) {
        websiteUrl = 'https://' + websiteUrl;
    }

    if (!isValidUrl(websiteUrl)) {
        console.error("Invalid URL");
        return null;
    }

    // If the URL is of the pattern /udemy.com/course-dashboard-redirect/?course_id=\d+/,
    // we reconstruct the URL to access its public content
    const dashboardRedirectPattern = /udemy\.com\/course-dashboard-redirect\/\?course_id=(\d+)/;
    const courseIdMatch = websiteUrl.match(dashboardRedirectPattern);
    if (courseIdMatch) {
        websiteUrl = `https://www.udemy.com/course/${courseIdMatch[1]}`;
    }

    const response = await fetch(websiteUrl, {
        method: 'GET',
        headers: {
            'User-Agent': 'python-requests/2.31.0', 
            'Accept-Encoding': 'gzip, deflate', 
            'Accept': '*/*', 
            'Connection': 'keep-alive'
        },
        redirect: 'follow',
    });

    if (!response.ok) {
        console.error(`Error fetching URL: ${response.status}`);
        return null;
    }

    console.log(`Fetched URL: ${websiteUrl}`);
    return response.text();
}

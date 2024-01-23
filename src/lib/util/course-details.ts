export function getCourseIdAndTitle(websiteText: string) {
    const patternId = /\/(\d+)_/;
    const patternTitle = /<meta name="title" content="([^"]+)">/;
    
    const matchId = websiteText.match(patternId);
    const matchTitle = websiteText.match(patternTitle);

    const courseId = matchId ? matchId[1] : null;
    const courseTitle = matchTitle ? matchTitle[1] : null;

    return { courseId, courseTitle };
}

export function isValidUrl(websiteUrl: string) {
    const patternWithId = /^https:\/\/www\.udemy\.com\/course-dashboard-redirect\/\?course_id=\d+$/;
    const patternWithCourseLink = /^https:\/\/www\.udemy\.com\/course\/[^/]+\//;

    return patternWithId.test(websiteUrl) || patternWithCourseLink.test(websiteUrl);
}

// function getWebsiteText(websiteUrl: string) {
//     const response = UrlFetchApp.fetch(websiteUrl);
//     return response.getContentText();
// }
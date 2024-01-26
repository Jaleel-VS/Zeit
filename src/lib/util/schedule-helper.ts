import fetch from 'node-fetch';

interface Lecture {
    can_be_previewed: boolean;
    content_summary: string;
    description: string;
    id: number;
    icon_class: string;
    is_coding_exercise: boolean;
    has_linked_workspace: boolean;
    landing_page_url: string | null;
    video_asset_id: number;
    preview_url: string;
    learn_url: string;
    title: string;
    object_index: number;
    item_type: string;
}

interface Section {
    content_length_text: string;
    content_length: number;
    index: number;
    items: Lecture[];
    lecture_count: number;
    title: string;
}

interface CurriculumContextData {
    sections: Section[];
}

interface CurriculumContext {
    data: CurriculumContextData;
}

interface ApiResponse {
    curriculum_context: CurriculumContext;
}

const CURRICULUM_ENDPOINT = "https://www.udemy.com/api-2.0/course-landing-components/???/me/?components=curriculum_context";

export async function getLectures(courseId: string): Promise<Record<string, Lecture[]>> {
    const endpointUrl = CURRICULUM_ENDPOINT.replace("???", courseId.toString());
    try {
        const response = await fetch(endpointUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: ApiResponse = await response.json() as ApiResponse;
        const sections = data.curriculum_context.data.sections;

        const courseDetail: Record<string, Lecture[]> = {};
        for (const section of sections) {
            courseDetail[section.title] = section.items;
            // console.log(section.title);
        }

        return courseDetail;
    } catch (error) {
        console.error('Error fetching course details:', error);
        throw error;
    }
}
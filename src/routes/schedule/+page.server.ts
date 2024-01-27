import { getSchedule } from '$lib/util/helpme';
import type { PageServerLoad } from '../$types';

export const load = (async () => {
    const currentDate = new Date();
    const schedule = getSchedule(
        1.5,
        0,
        currentDate,
        false,
        1.0
    )
    return {};
}) satisfies PageServerLoad;
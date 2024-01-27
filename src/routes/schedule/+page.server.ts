import { getSchedule } from '$lib/util/helpme';
import type { PageServerLoad } from './$types';

export const load = (async () => {
    const schedule = await getSchedule(
        1,
        30,
        new Date(),
        false,
        1.0,
    );
    return {
        schedule,
    };
}) satisfies PageServerLoad;
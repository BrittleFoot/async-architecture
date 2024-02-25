import { ensureAuthenticated } from '$lib';


export const load = async ({ locals }) => {
    await ensureAuthenticated(await locals.auth());
    return {};
};
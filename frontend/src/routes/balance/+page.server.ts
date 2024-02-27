import { ensureAuthenticated } from '$lib/auth';

export const load = async ({ locals }) => {
	await ensureAuthenticated(await locals.auth());
	return {};
};

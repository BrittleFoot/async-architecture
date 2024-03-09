import { ensureAuthenticated } from '$lib/auth';

export const load = async ({ locals }) => {
	let { tokenInfo } = await ensureAuthenticated(await locals.auth());
	return {
		tokenInfo
	};
};

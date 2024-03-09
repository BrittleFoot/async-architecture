import { ensureAuthenticated } from '$lib/auth';
import { getMe } from '$lib/utils.js';

export const load = async ({ locals }) => {
	let { tokenInfo, session } = await ensureAuthenticated(await locals.auth());
	let user = await getMe(session);
	return {
		tokenInfo,
		user
	};
};

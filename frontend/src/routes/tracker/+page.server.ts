import { ensureAuthenticated } from '$lib/auth';
import { getMe } from '$lib/utils.js';

export const load = async ({ locals }) => {
	let { tokenInfo, session } = await ensureAuthenticated(await locals.auth());
	return {
		accessToken: tokenInfo.accessToken,
		user: await getMe(session),
	};
};

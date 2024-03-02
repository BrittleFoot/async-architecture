import { ensureAuthenticated } from '$lib/auth';
import { UserService } from '$lib/api/user.js';

export const load = async ({ locals }) => {
	let { tokenInfo } = await ensureAuthenticated(await locals.auth());

	return {
		accessToken: tokenInfo.accessToken,
		me: await new UserService(tokenInfo.accessToken).getMe()
	};
};

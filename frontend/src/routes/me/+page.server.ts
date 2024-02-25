import { ensureAuthenticated } from '$lib';
import { UserService } from '$lib/api/user.js';

export const load = async ({ locals }) => {
	let { tokenInfo } = await ensureAuthenticated(await locals.auth());

	return {
		me: await new UserService(tokenInfo.accessToken).getMe()
	};
};

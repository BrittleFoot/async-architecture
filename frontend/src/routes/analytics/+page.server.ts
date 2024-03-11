import { ensureAuthenticated } from '$lib/auth';
import { getMe } from '$lib/utils.js';
import { fail, redirect } from '@sveltejs/kit';

export const load = async ({ locals }) => {
	let { tokenInfo, session } = await ensureAuthenticated(await locals.auth());
	let user = await getMe(session);
	if (!user?.roles?.includes('admin')) {
		return redirect(301, '/');
	}
	return {
		tokenInfo,
		user
	};
};

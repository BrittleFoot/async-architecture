import { getMe } from '$lib/utils.js';

export const load = async (event) => {
	let session = await event.locals.auth();
	let me: User | null = null;
	try {
		me = await getMe(session);
	} catch (e) {
		console.error(e);
	}
	return {
		session: session,
		user: me
	};
};

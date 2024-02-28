import { getMe } from '$lib/utils.js';

export const load = async (event) => {
	let session = await event.locals.auth()

	return {
		session: session,
		user: await getMe(session),
	};
};

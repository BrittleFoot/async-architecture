import { signIn } from '../../auth';
import type { Actions } from './$types';
import { ensureNotAuthenticated } from '$lib/auth';

export const actions: Actions = {
	default: async (event) => {
		ensureNotAuthenticated(await event.locals.auth());
		await signIn(event);
	}
};

export const load = async (event) => {
	ensureNotAuthenticated(await event.locals.auth());
};

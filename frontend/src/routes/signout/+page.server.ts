import { signOut } from '../../auth';
import type { Actions } from './$types';
import { AuthService } from '$lib/api/auth';
import { ensureAuthenticated } from '$lib/auth';

export const actions: Actions = {
	default: async (event) => {
		let { tokenInfo } = await ensureAuthenticated(await event.locals.auth(), '/');

		try {
			await new AuthService().signOut(tokenInfo);
		} catch (e) {
			console.error('error revoking token', e);
		}

		await signOut(event);
	}
};

export const load = async (event) => {
	await ensureAuthenticated(await event.locals.auth(), '/');
};

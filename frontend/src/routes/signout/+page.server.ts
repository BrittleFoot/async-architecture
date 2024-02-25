import { redirect } from '@sveltejs/kit';
import { signOut } from '../../auth';
import type { Actions } from './$types';
import { getTokenInfoBySessionToken } from '$lib/db/methods';
import { AuthService } from '$lib/api/auth';

export const actions: Actions = {
	default: async (event) => {
		let session = await event.locals.auth();

		if (!session?.user) {
			throw redirect(302, '/');
		}

		let sessionToken = event.cookies.get('authjs.session-token');
		if (sessionToken) {
			let authService = new AuthService(null);
			try {
				await authService.revokeToken(sessionToken);
			} catch (e) {
				console.error('error revoking token', e);
			}
		}

		await signOut(event);
	}
};

export const load = async (event) => {
	let session = await event.locals.auth();

	if (!session?.user) {
		throw redirect(302, '/');
	}
};

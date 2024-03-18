import type { Actions } from './$types';
import { ensureNotAuthenticated } from '$lib/auth';
import { AuthService } from '$lib/api/auth';
import { RequestError } from '$lib';

type RegistraionErrors = {
	username?: string;
	password?: string;
};

export const actions: Actions = {
	register: async (event) => {
		ensureNotAuthenticated(await event.locals.auth());

		let formData = await event.request.formData();

		let regInfo = {
			username: formData.get('username')?.toString() ?? '',
			password: formData.get('password')?.toString() ?? '',
			isAdmin: formData.get('isAdmin') ?? false,
			isManager: formData.get('isManager') ?? false,
			isPerformer: formData.get('isPerformer') ?? false
		};

		let errors: RegistraionErrors = {};
		if (!regInfo.username) {
			errors.username = 'Username is required';
		}
		if (!regInfo.password.length) {
			errors.password = 'Password is required';
		}

		if (Object.keys(errors).length > 0) {
			return {
				errors
			};
		}

		let roles = [];
		if (regInfo.isAdmin) {
			roles.push('admin');
		}
		if (regInfo.isManager) {
			roles.push('manager');
		}
		if (regInfo.isPerformer) {
			roles.push('performer');
		}

		try {
			let user = await new AuthService().signUp(regInfo.username, regInfo.password, roles);
			return {
				user
			};
		} catch (e) {
			if (e instanceof RequestError)
				return {
					errors: e.data
				};
			throw e;
		}
	}
};

export const load = async (event) => {
	ensureNotAuthenticated(await event.locals.auth());
};

import { RequestError } from '$lib';
import { isHttpError } from '@sveltejs/kit';

export function checkUserRoles(user: User, roles: UserRole[]) {
	return roles.some((role) => user.roles.includes(role));
}

export function getErrorMsg(e: any) {
	if (isHttpError(e)) {
		return `${e.body.message}: ${e.body.data?.detail?.detail}`;
	}

	if (e instanceof RequestError) {
		return e.message;
	}

	let er = e as { status: number; body: { message: string } };
	return `${er.status}: ${er.body.message}`;
}

import { redirect } from '@sveltejs/kit';
import { getTokenInfoBySessionToken, type TokenInfo } from './db/methods';
import type { AdapterSession } from '@auth/core/adapters';
import type { Session } from '@auth/sveltekit';

export async function ensureAuthenticated(
	session: Session | null,
	redirectTo: string = '/signin'
): Promise<{ tokenInfo: TokenInfo; session: Session }> {
	let trueSession = session as (Session & AdapterSession) | null;

	if (!trueSession || !trueSession?.user || !trueSession.sessionToken) {
		throw redirect(302, redirectTo);
	}

	let tokenInfo = await getTokenInfoBySessionToken(trueSession.sessionToken);
	if (!tokenInfo) {
		throw redirect(302, redirectTo);
	}

	return { tokenInfo, session: trueSession };
}

export async function getTokenInfo(session: Session | null): Promise<{ tokenInfo?: TokenInfo }> {
	let trueSession = session as (Session & AdapterSession) | null;

	if (!trueSession || !trueSession?.user || !trueSession.sessionToken) {
		return {}
	}

	let tokenInfo = await getTokenInfoBySessionToken(trueSession.sessionToken);
	if (!tokenInfo) {
		return {}
	}

	return { tokenInfo };
}

export function ensureNotAuthenticated(session: Session | null, redirectTo: string = '/') {
	if (session && session.user) {
		throw redirect(302, redirectTo);
	}
}

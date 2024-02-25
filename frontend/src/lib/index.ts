import type { Session } from '@auth/sveltekit';
import { redirect, type NumericRange, error, fail } from '@sveltejs/kit';
import { getTokenInfoBySessionToken, type TokenInfo } from './db/methods';
import type { AdapterSession } from '@auth/core/adapters';

export type DataWithDetail = {
	detail: string;
	headers: [string, string][];
};

export class RequestError extends Error {
	constructor(
		public message: string,
		public status: NumericRange<400, 599>,
		public data: DataWithDetail
	) {
		super(message);
		this.name = 'RequestError';
		this.status = status;
		this.data = data;
	}

	toServerError() {
		return error(this.status, { message: this.message, data: this.data });
	}
}

async function readBody(response: Response) {
	const contentType = response.headers.get('content-type');
	if (contentType && contentType.indexOf('application/json') !== -1) return response.json();

	return response.text().then((text) => {
		return { body: text };
	});
}

type ApiClientParams = {
	accessToken?: string;
	backendUrl: string;
};

class ApiClient {
	constructor(private params: ApiClientParams) {}

	async request<T>(url: string, options?: RequestInit): Promise<T> {
		try {
			return await this.unsafeRequest<T>(url, options);
		} catch (e) {
			if (e instanceof RequestError) throw e.toServerError();
			throw e;
		}
	}

	async unsafeRequest<T>(url: string, options?: RequestInit): Promise<T> {
		if (url.startsWith('/')) url = url.substring(1);
		var authBackend = this.params.backendUrl;
		if (authBackend.endsWith('/')) authBackend = authBackend.substring(0, authBackend.length - 1);

		url = `${authBackend}/${url}`;

		let authorization = (
			this.params.accessToken ? { Authorization: `Bearer ${this.params.accessToken}` } : {}
		) as HeadersInit;

		options = {
			...options,
			headers: {
				...options?.headers,
				...authorization
			}
		};

		let response = await fetch(url, options);

		if (!response.ok) {
			throw new RequestError(response.statusText, response.status as NumericRange<400, 599>, {
				detail: await readBody(response),
				headers: [...response.headers.entries()]
			});
		}

		return (await readBody(response)) as T;
	}
}

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

export function ensureNotAuthenticated(session: Session | null, redirectTo: string = '/') {
	if (session && session.user) {
		throw redirect(302, redirectTo);
	}
}

export default ApiClient;

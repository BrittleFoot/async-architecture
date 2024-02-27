import { type NumericRange, error } from '@sveltejs/kit';

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

export default ApiClient;

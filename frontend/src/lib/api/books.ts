import { PUBLIC_AUTH_BACKEND_URL } from '$env/static/public';
import ApiClient from '$lib';

export type Author = {
	id: number;
	name: string;
};

export type Book = {
	id: number;
	name: string;
	author: Author;
};

export class BookService {
	api: ApiClient;
	constructor(accessToken: string) {
		this.api = new ApiClient({ backendUrl: PUBLIC_AUTH_BACKEND_URL, accessToken });
	}
	async getBooks(): Promise<Book[]> {
		return await this.api.request<Book[]>('/api/v1/books/');
	}
}

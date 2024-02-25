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
		this.api = new ApiClient(accessToken);
	}
	async getBooks(): Promise<Book[]> {
		return await this.api.request<Book[]>('/api/v1/books/');
	}
}

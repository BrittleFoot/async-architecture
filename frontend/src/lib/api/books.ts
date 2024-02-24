import ApiClient from "$lib";
import type { Session } from "@auth/sveltekit";


export type Author = {
    id: number;
    name: string;
}

export type Book = {
    id: number;
    name: string;
    author: Author;
}

export class BookService {
    api: ApiClient;
    constructor(accessToken: string) {
        this.api = new ApiClient(accessToken);
    }
    async getBooks(): Promise<Book[]> {
        let books = await this.api.request("/api/v1/books");
        return books as Book[];
    }
}

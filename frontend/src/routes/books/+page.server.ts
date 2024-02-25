import { ensureAuthenticated } from '$lib';
import { BookService } from '$lib/api/books.js';

async function pageData(accessToken: string) {
	let bookService = new BookService(accessToken);

	return {
		books: await bookService.getBooks()
	};
}

export const load = async ({ locals }) => {
	let { tokenInfo } = await ensureAuthenticated(await locals.auth());

	return {
		...(await pageData(tokenInfo.accessToken))
	};
};

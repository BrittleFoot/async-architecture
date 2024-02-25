import { RequestError } from '$lib';
import { BookService } from '$lib/api/books.js';
import { getTokenInfoBySessionToken } from '$lib/db/methods.js';
import { error, redirect } from '@sveltejs/kit';

async function pageData(accessToken: string) {
	let bookService = new BookService(accessToken);

	try {
		let books = await bookService.getBooks();

		return {
			books: books
		};
	} catch (e) {
		if (e instanceof RequestError) throw error(e.status, { message: e.message, data: e.data });
		else throw e;
	}
}

export const load = async ({ locals, cookies }) => {
	let session = await locals.auth();
	let sessionToken = cookies.get('authjs.session-token');

	if (!session?.user || !sessionToken) {
		throw redirect(302, '/signin');
	}

	let tokenInfo = await getTokenInfoBySessionToken(sessionToken);
	if (!tokenInfo) {
		throw redirect(302, '/signin');
	}

	return {
		...(await pageData(tokenInfo.accessToken))
	};
};

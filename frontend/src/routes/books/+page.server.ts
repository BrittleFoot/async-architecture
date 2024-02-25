import { RequestError, ensureAuthenticated } from '$lib';
import { BookService } from '$lib/api/books.js';

async function pageData(accessToken: string) {
    let bookService = new BookService(accessToken);

    try {
        return {
            books: await bookService.getBooks()
        };
    } catch (e) {
        if (e instanceof RequestError)
            throw e.toServerError();

        throw e;
    }
}

export const load = async ({ locals }) => {
    let { tokenInfo } = await ensureAuthenticated(await locals.auth());

    return {
        ...(await pageData(tokenInfo.accessToken))
    };
};

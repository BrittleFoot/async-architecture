import connectionPool from '$lib/db/connect.js';
import { getAccessTokenBySessionToken } from '$lib/db/methods.js';
import { redirect } from '@sveltejs/kit';


export const load = async ({ locals, cookies }) => {
    let session = await locals.auth();

    let sessionToken = cookies.get('authjs.session-token');

    if (!session?.user || !sessionToken) {
        throw redirect(302, '/signin');
    }

    let accessToken = await getAccessTokenBySessionToken(sessionToken);
    console.log('accessToken', accessToken);
    return {
        accessToken: accessToken,
    };
};

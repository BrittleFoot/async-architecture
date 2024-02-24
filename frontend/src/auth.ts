import { SvelteKitAuth } from '@auth/sveltekit';
import { CLIENT_ID, CLIENT_SECRET } from '$env/static/private';
import type { OAuth2Config } from "@auth/core/providers"
import PostgresAdapter from '@auth/pg-adapter';
import connectionPool from '$lib/db/connect';

type User = {
    id: string;
    name: string;
    token: string;
};

export const { handle, signIn, signOut } = SvelteKitAuth({
    providers: [
        {
            id: "popug-auth",
            name: "Popug Auth",
            type: "oauth",
            issuer: "http://127.0.0.1:8000",
            authorization: {
                url: "http://127.0.0.1:8000/oauth/authorize/",
                params: { scope: "read write" },
            },
            token: "http://127.0.0.1:8000/oauth/token/",
            userinfo: "http://127.0.0.1:8000/api/v1/users/me/",
            clientId: CLIENT_ID,
            clientSecret: CLIENT_SECRET,
        } satisfies OAuth2Config<User>,
    ],
    adapter: PostgresAdapter(connectionPool),
});
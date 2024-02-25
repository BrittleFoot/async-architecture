import { SvelteKitAuth } from '@auth/sveltekit';
import { CLIENT_ID, CLIENT_SECRET } from '$env/static/private';
import type { OAuth2Config } from '@auth/core/providers';
import PostgresAdapter from '@auth/pg-adapter';
import connectionPool from '$lib/db/connect';
import { AuthService } from '$lib/api/auth';

type User = {
	id: string;
	name: string;
	token: string;
};

export const { handle, signIn, signOut } = SvelteKitAuth({
	providers: [
		{
			id: 'popug-auth',
			name: 'Popug Auth',
			type: 'oauth',
			issuer: 'http://127.0.0.1:8000',
			authorization: {
				url: 'http://127.0.0.1:8000/oauth/authorize/',
				params: { scope: 'read write' }
			},
			token: 'http://127.0.0.1:8000/oauth/token/',
			userinfo: 'http://127.0.0.1:8000/api/v1/users/me/',
			clientId: CLIENT_ID,
			clientSecret: CLIENT_SECRET
		} satisfies OAuth2Config<User>
	],
	adapter: PostgresAdapter(connectionPool),
	callbacks: {
		async signIn({ account, user }) {
			if (account && user && user.id) {
				await new AuthService().signIn(Number.parseInt(user.id), account);
			}
			return true;
		},
		async session({ session }) {
            await new AuthService().refreshTokenIfNeeded(session.sessionToken);
			return session;
		}
	}
});

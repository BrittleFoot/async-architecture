import { SvelteKitAuth } from '@auth/sveltekit';
import { env as envPrivate } from '$env/dynamic/private';
import { env } from '$env/dynamic/public';
import type { OAuth2Config } from '@auth/core/providers';
import PostgresAdapter from '@auth/pg-adapter';
import getConnectionPool from '$lib/db/connect';
import { AuthService } from '$lib/api/auth';

function isUUID(str: string): boolean {
	const regex =
		/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89ABab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$/;
	return regex.test(str);
}

export const { handle, signIn, signOut } = SvelteKitAuth({
	providers: [
		{
			id: 'popug-auth',
			name: 'Popug Auth',
			type: 'oauth',
			issuer: env.PUBLIC_AUTH_BACKEND_URL,
			authorization: {
				url: env.PUBLIC_AUTH_BACKEND_URL + '/oauth/authorize/',
				params: { scope: 'read write' }
			},
			token: env.PUBLIC_AUTH_BACKEND_URL + '/oauth/token/',
			userinfo: env.PUBLIC_AUTH_BACKEND_URL + '/api/v1/users/me/',
			clientId: envPrivate.CLIENT_ID,
			clientSecret: envPrivate.CLIENT_SECRET
		} satisfies OAuth2Config<User>
	],
	trustHost: true,
	adapter: PostgresAdapter(getConnectionPool()),
	callbacks: {
		async signIn({ account, user, profile }) {
			let firstTimeSignIn = isUUID(user.id ?? '');
			if (!firstTimeSignIn && account && user && user.id) {
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

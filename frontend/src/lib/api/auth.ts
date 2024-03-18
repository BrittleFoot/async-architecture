import { env as envPrivate } from '$env/dynamic/private';
import { env } from '$env/dynamic/public';
import ApiClient from '$lib';
import { getTokenInfoBySessionToken, updateUserAccount, type TokenInfo } from '$lib/db/methods';
import type { Account } from '@auth/sveltekit';

type TokenResponse = {
	access_token: string;
	expires_in: number;
	token_type: 'bearer';
	scope: string;
	refresh_token: string;
};

export class AuthService {
	api: ApiClient;

	constructor() {
		this.api = new ApiClient({ backendUrl: env.PUBLIC_AUTH_BACKEND_URL });
	}

	async signIn(userId: number, account: Account) {
		await updateUserAccount(userId, account);
	}

	async signOut(tokenInfo?: TokenInfo) {
		await this.revokeToken(tokenInfo);
	}

	async signUp(username: string, password: string, roles: string[]) {
		return await this.api.unsafeRequest<User>('/api/v1/users/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, password, roles })
		});
	}

	async revokeToken(tokenInfo?: TokenInfo) {
		if (!tokenInfo) {
			return;
		}

		let formData = new FormData();
		formData.append('token', tokenInfo.accessToken);
		formData.append('client_id', envPrivate.CLIENT_ID);
		formData.append('client_secret', envPrivate.CLIENT_SECRET);

		await this.api.request('/oauth/revoke_token/', {
			method: 'POST',
			body: formData
		});
		console.log('token revoked');
	}

	public isTokenExpired(tokenInfo: TokenInfo): boolean {
		let now = convertDateToSeconds(new Date());
		let expires = tokenInfo.expiresAt.getTime();

		return now > expires;
	}

	async refreshToken(tokenInfo: TokenInfo) {
		let formData = new FormData();
		formData.append('grant_type', 'refresh_token');
		formData.append('refresh_token', tokenInfo.refreshToken);
		formData.append('client_id', envPrivate.CLIENT_ID);
		formData.append('client_secret', envPrivate.CLIENT_SECRET);

		let token = await this.api.request<TokenResponse>('/oauth/token/', {
			method: 'POST',
			body: formData
		});

		console.log('token refreshed');

		await updateUserAccount(tokenInfo.userId, {
			access_token: token.access_token,
			token_type: 'bearer',
			scope: token.scope,
			refresh_token: token.refresh_token,
			expires_at: getExpiredAt(token.expires_in),
			provider: 'popug-auth',
			type: 'oauth',
			providerAccountId: '1'
		});
	}

	async refreshTokenIfNeeded(sessionToken: string) {
		let tokenInfo = await getTokenInfoBySessionToken(sessionToken);

		if (tokenInfo && this.isTokenExpired(tokenInfo)) {
			await this.refreshToken(tokenInfo);
		}
	}
}

function convertDateToSeconds(date: Date): number {
	return Math.floor(date.getTime() / 1000);
}

function getExpiredAt(expiresIn: number = 0): number {
	return convertDateToSeconds(new Date(Date.now() + expiresIn * 1000));
}

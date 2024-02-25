import type { Account, User } from '@auth/sveltekit';
import connectionPool from './connect';
import type { AdapterUser } from '@auth/core/adapters';

export type TokenInfo = {
	userId: number;
	sessionToken: string;
	accessToken: string;
	refreshToken: string;
	expiresAt: Date;
};

export async function getUserAccount(userId: string) {
	let sql = `SELECT * FROM accounts WHERE "userId" = $1`;
	let result = await connectionPool.query(sql, [userId]);
	return result.rowCount === 0 ? null : result.rows[0];
}

export async function updateUserAccount(userId: number, account: Account) {
	let sql = `UPDATE accounts
        SET
            "access_token" = $2,
            "token_type" = $3,
            "scope" = $4,
            "refresh_token" = $5,
            "expires_at" = $6,
            "provider" = $7,
            "type" = $8
        WHERE "userId" = $1;
    `;

	await connectionPool.query(sql, [
		userId,
		account.access_token,
		account.token_type,
		account.scope,
		account.refresh_token,
		account.expires_at,
		account.provider,
		account.type
	]);
}

export async function getTokenInfoBySessionToken(sessionToken: string): Promise<TokenInfo | null> {
	let sql = `select
            sessions."userId",
            sessions."sessionToken",
            accounts."access_token" as "accessToken",
            accounts."refresh_token" as "refreshToken",
            accounts."expires_at" as "expiresAt"
        from sessions
        left join accounts on sessions."userId" = accounts."userId"
        where sessions."sessionToken" = $1
    `;
	let result = await connectionPool.query(sql, [sessionToken]);
	if (result.rowCount === 0) {
		return null;
	}
	return {
		userId: result.rows[0].userId,
		sessionToken: result.rows[0].sessionToken,
		accessToken: result.rows[0].accessToken,
		refreshToken: result.rows[0].refreshToken,
		expiresAt: new Date(Number.parseInt(result.rows[0].expiresAt))
	};
}

export async function clearTokenInfoBySessionToken(accessToken: string) {
	let sql = `UPDATE accounts
        SET "accessToken" = '', "refreshToken" = ''
        WHERE "sessionToken" = $1;
`;
	// await connectionPool.query(sql, [sessionToken]);
}

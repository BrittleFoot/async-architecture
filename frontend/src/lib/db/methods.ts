import connectionPool from "./connect";


export async function getAccessTokenBySessionToken(sessionToken: string) {
    let sql = ` select accounts."access_token" as "accessToken"
        from sessions
        left join accounts on sessions."userId" = accounts."userId"
        where sessions."sessionToken" = $1
    `;
    let result = await connectionPool.query(sql, [sessionToken]);
    return result.rowCount === 0 ? null : result.rows[0].accessToken;
}
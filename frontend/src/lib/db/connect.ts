import pg from 'pg';
import { env } from '$env/dynamic/private';

let connectionPool: pg.Pool | null = null;

const getConnectionPool = (): pg.Pool => {
	if (!connectionPool) {
		connectionPool = new pg.Pool({ connectionString: env.DATABASE_URL });

		connectionPool
			.connect()
			.then(() => {
				console.log('PG: Connected to PostgreSQL database');
			})
			.catch((err) => {
				console.error('PG: Error connecting to PostgreSQL database', err);
			});
	}

	return connectionPool;
};

export default getConnectionPool;

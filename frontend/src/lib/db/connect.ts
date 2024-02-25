import pg from 'pg';
import { DATABASE_URL } from '$env/static/private';

let connectionPool = new pg.Pool({ connectionString: DATABASE_URL });

connectionPool
	.connect()
	.then(() => {
		console.log('PG: Connected to PostgreSQL database');
	})
	.catch((err) => {
		console.error('PG: Error connecting to PostgreSQL database', err);
	});

export default connectionPool;

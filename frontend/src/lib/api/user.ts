import { env } from '$env/dynamic/public';
import ApiClient from '$lib';

export class UserService {
	api: ApiClient;

	constructor(accessToken: string) {
		this.api = new ApiClient({ backendUrl: env.PUBLIC_AUTH_BACKEND_URL, accessToken });
	}

	async getMe() {
		return await this.api.request<User>('/api/v1/users/me/');
	}

	async listUsers() {
		return await this.api.request<User[]>('/api/v1/users/');
	}

	async editUser(user: UserEdit) {
		return await this.api.jsonRequest<User>('PUT', `/api/v1/users/${user.id}/`, user);
	}
}

import { PUBLIC_TRACKER_BACKEND_URL } from '$env/static/public';
import ApiClient from '$lib';

export type Task = {
	id: number;
	summary: string;
	status: string;
	performer: TaskUser;
	completionDate: string;
	created: string;

	optimistic?: boolean;
};

export type TaskUser = {
	username: string;
	publicId: string;
};

export class TrackerService {
	api: ApiClient;

	constructor(accessToken?: string) {
		this.api = new ApiClient({ backendUrl: PUBLIC_TRACKER_BACKEND_URL, accessToken });
	}

	async getTasks(hideCompleted?: boolean): Promise<Task[]> {
		var url = '/api/v1/tasks/';
		if (hideCompleted) {
			url += '?status=new';
		}
		return await this.api.request<Task[]>(url);
	}

	async createTask(summary: string): Promise<Task> {
		return await this.api.request<Task>('/api/v1/tasks/', {
			method: 'POST',
			body: JSON.stringify({ summary }),
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	async completeTask(task: Task): Promise<Task> {
		return await this.api.request<Task>(`/api/v1/tasks/${task.id}/`, {
			method: 'PUT',
			body: '{}',
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	async reassignTasks(): Promise<void> {
		return await this.api.request<void>(`/api/v1/tasks/reassign/`, {
			method: 'POST'
		});
	}
}

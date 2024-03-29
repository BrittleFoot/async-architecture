import { env } from '$env/dynamic/public';
import ApiClient from '$lib';

export type Task = {
	id: number;
	taskId: string;
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
		this.api = new ApiClient({ backendUrl: env.PUBLIC_TRACKER_BACKEND_URL, accessToken });
	}

	async getTasks(hideCompleted?: boolean): Promise<Task[]> {
		var url = '/api/v2/tasks/';
		if (hideCompleted) {
			url += '?status=new';
		}
		return await this.api.request<Task[]>(url);
	}

	async createTask(summary: string): Promise<Task> {
		return await this.api.jsonRequest<Task>('POST', '/api/v1/tasks/', { summary });
	}

	async createTaskV2(taskId: string, summary: string): Promise<Task> {
		return await this.api.jsonRequest<Task>('POST', '/api/v2/tasks/', { taskId, summary });
	}

	async completeTask(task: Task): Promise<Task> {
		return await this.api.jsonRequest<Task>('PUT', `/api/v2/tasks/${task.id}/`, {});
	}

	async reassignTasks(): Promise<void> {
		return await this.api.jsonRequest<void>('POST', `/api/v1/tasks/reassign/`, {});
	}
}

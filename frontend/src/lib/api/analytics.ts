import { PUBLIC_ANALYTICS_BACKEND_URL } from '$env/static/public';
import ApiClient from '$lib';

export interface Task {
	id: number;
	publicId: string;
	taskId: string;
	summary: string;
	fee: string; // decimal
	reward: string; // decimal
	created: string;
}

export interface TransactionUser {
	id: number;
	publicId: string;
	username: string;
}

export interface Transaction {
	id: number;
	task: Task | null;
	user: TransactionUser;
	publicId: string;
	type: string;
	comment: string;
	credit: string; // decimal
	debit: string; // decimal
	created: string;
}

export interface Day {
	id: number;
	publicId: string;
	profit: number;
	name: string;
	totalTransactions: number;
	totalProfit: number;
	totalExpense: number;
	highestRewardTransaction: Transaction | null;
}

export interface DayInfo {
	id: number;
	publicId: number;
	name: string;
	users: UserInfo[];
}

export interface UserInfo {
	id: number;
	publicId: string;
	username: string;
	transactions: TransactionInfo[];
	totalProfit: number;
	totalExpense: number;
	todayBalance: number;
}

export interface TransactionInfo {
	id: number;
	publicId: string;
	dayId: number;
	type: string;
	credit: string;
	debit: string;
	created: string;
}

export class AnalyticsService {
	api: ApiClient;

	constructor(accessToken?: string) {
		this.api = new ApiClient({ backendUrl: PUBLIC_ANALYTICS_BACKEND_URL, accessToken });
	}

	async getDayAnalytics() {
		return await this.api.request<Day[]>(`/api/v1/analytics/day/`);
	}

	async getPerformersAnalytics() {
		return await this.api.request<DayInfo[]>(`/api/v1/analytics/performer/`);
	}
}

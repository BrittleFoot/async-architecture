import { PUBLIC_BILLING_BACKEND_URL } from '$env/static/public';
import ApiClient from '$lib';

export interface Payment {
	id: number;
	publicId: string;
	amount: string; // decimal
	status: string;
	created: Date;
}

export interface Transaction {
	id: number;
	publicId: string;
	type: string;
	comment: string;
	credit: string; // decimal
	debit: string; // decimal
	created: Date;
}

export interface BillingCycle {
	id: number;
	publicId: string;
	user: UserLight;
	status: string;
	closeDate: Date;
	transactions: Transaction[];
	payments: Payment[];
	created: Date;
	modified: Date;
}

export interface Day {
	id: number;
	name: string;
	billingCycles: BillingCycle[];
	profit?: string; // decimal
}

export interface DayLight {
	id: number;
	name: string;
	profit?: string; // decimal
}

export interface UserLight {
	publicId: number;
	username: string;
}

export class BillingService {
	api: ApiClient;

	constructor(accessToken?: string) {
		this.api = new ApiClient({ backendUrl: PUBLIC_BILLING_BACKEND_URL, accessToken });
	}

	async getDays(): Promise<DayLight[]> {
		var url = '/api/v1/billing/day/?calendar=1';
		return await this.api.request<DayLight[]>(url);
	}

	async getFullDays(): Promise<Day[]> {
		var url = '/api/v1/billing/day/';
		return await this.api.request<Day[]>(url);
	}

	async getDay(id: number): Promise<Day> {
		return await this.api.request<Day>(`/api/v1/billing/day/${id}/`);
	}

	async endDay(): Promise<Day> {
		return await this.api.jsonRequest<Day>('POST', `/api/v1/billing/day/`, {});
	}
}

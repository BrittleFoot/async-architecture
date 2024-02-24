import { dev } from "$app/environment";
import type { Session } from "@auth/sveltekit";


class RequestError extends Error {
    constructor(public message: string, public status: number, public data: object) {
        super(message);
        this.name = "RequestError";
        this.status = status;
        this.data = data;
    }
}

class ApiClient {

    constructor(public accessToken: string) {
        this.accessToken = accessToken;
    }

    request = async (url: string, options?: RequestInit): Promise<object> => {

        if (dev) {
            if (url.startsWith("/"))
                url = url.substring(1);
            url = `http://localhost:8000/${url}`;
        }


        options = {
            ...options,
            headers: {
                ...options?.headers,
                "Authorization": `Bearer ${this.accessToken}`,
            },
        };

        let response = await fetch(url, options);
        if (!response.ok) {
            throw new RequestError(response.statusText, response.status, await response.json());
        }
        return await response.json();
    };

}

export default ApiClient;

type UserRole = "admin" | "manager" | "performer";

type User = {
	id: string;
	username: string;
	name: string;
	token: string;
	roles: UserRole[];
	publicId: string;
};



type UserEdit = {
	id: string;
	username: string;
	roles: UserRole[];
};
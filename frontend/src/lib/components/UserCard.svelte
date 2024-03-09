<script lang="ts">
	import { getErrorMsg } from '$lib/typeUtils';

	export let user: User;
	export let editor: User;
	export let update: (user: UserEdit) => Promise<User>;

	type UserForm = {
		id: string;
		username: string;
		isAdmin: boolean;
		isManager: boolean;
		isPerformer: boolean;
	};

	let { id, username, isAdmin, isManager, isPerformer } = fillForm(user);

	let roles: UserRole[] = [];
	$: {
		roles = [];
		if (isAdmin) roles.push('admin');
		if (isManager) roles.push('manager');
		if (isPerformer) roles.push('performer');
	}

	let status: 'idle' | 'pending' | 'success' | 'error' = 'idle';
	let errormsg = '';

	$: newUser = { id, username, roles } as UserEdit;

	$: isEdited = user.username !== newUser.username || !setsEqual(user.roles, newUser.roles);

	$: adminEditing = editor.roles.includes('admin');

	function setsEqual(a: any[], b: any[]) {
		return a.length === b.length && a.every((v, i) => b.includes(v));
	}

	async function handelSubmit(event: Event) {
		status = 'pending';
		try {
			user = await update({ id, username, roles } as UserEdit);

			status = 'success';
		} catch (error) {
			refillForm(user);
			console.log(user);
			errormsg = getErrorMsg(error);
			console.log(errormsg);
			status = 'error';
		}
	}

	function fillForm(user: User): UserForm {
		return {
			id: user.id,
			username: user.username,
			isAdmin: user.roles.includes('admin'),
			isManager: user.roles.includes('manager'),
			isPerformer: user.roles.includes('performer')
		};
	}

	function refillForm(user: User) {
		let userForm = fillForm(user);
		id = userForm.id;
		username = userForm.username;
		isAdmin = userForm.isAdmin;
		isManager = userForm.isManager;
		isPerformer = userForm.isPerformer;
	}
</script>

<div class="card">
	<form on:submit|preventDefault={handelSubmit}>
		<input type="text" placeholder="Username" bind:value={username} />

		<label for="admin">
			<input type="checkbox" bind:checked={isAdmin} disabled={!adminEditing} />
			Admin
		</label>
		<label for="manager">
			<input type="checkbox" bind:checked={isManager} disabled={!adminEditing} />
			Manager
		</label>

		<label for="performer">
			<input type="checkbox" bind:checked={isPerformer} disabled={!adminEditing} />
			Performer
		</label>

		<input
			type="submit"
			value="Update"
			class="margin-0"
			disabled={!isEdited}
			class:secondary={!isEdited}
			aria-busy={status === 'pending'}
		/>
	</form>
</div>

<style>
	.card {
		display: flex;
		flex-direction: column;
		gap: 1em;
		padding: 1em;

		max-width: calc(100% / 3 - 1em);
		min-width: 10em;
		background-color: #1a202ccc;
		border-radius: 0.5em;

		box-shadow: 0 0 0.5em 0.1em #000000aa;
	}

	.margin-0 {
		margin: 0.1em 0;
	}
</style>

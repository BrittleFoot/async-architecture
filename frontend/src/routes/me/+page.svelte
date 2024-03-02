<script lang="ts">
	import { UserService } from '$lib/api/user.js';
	import UserCard from '$lib/components/UserCard.svelte';
	import { checkUserRoles } from '$lib/typeUtils';
	import { onMount } from 'svelte';

	export let data;

	const userService = new UserService(data.accessToken);

	let me = data.me;
	let users: User[] = [];

	$: meAdmin = checkUserRoles(me, ['admin']);

	onMount(async () => {
		await refreshManagedUsers();
	});

	async function update(user: UserEdit): Promise<User> {
		let updated = await userService.editUser(user);

		if (updated.publicId === me.publicId) {
			me = updated;
			await refreshManagedUsers();
		}
		return updated;
	}

	async function refreshManagedUsers() {
		if (!meAdmin) return;
		users = (await userService.listUsers()).filter(u => u.publicId !== me.publicId);
	}


</script>

<h1>🦜 {me.name}</h1>

<h2>Edit personal info</h2>

	<UserCard user={me} {update}/>


{#if meAdmin}
<br/>
<h2>Manage users</h2>

<div class="cards">
	{#each users as user}
		<UserCard {user} {update}/>
	{/each}
</div>

{/if}


<style>
	.cards {
		display: flex;
		flex-wrap: wrap;
		gap: 1em;
	}
</style>
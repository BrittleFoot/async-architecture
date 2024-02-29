<script lang="ts">
	import { faker } from '@faker-js/faker';
	import { onMount } from 'svelte';

	export let form;

	let name = "";
	onMount(() => {
		name = faker.person.firstName();
	});
</script>

<h1>🤗 Sign Up</h1>

{#if form?.user}
	<p>Welcome, {form.user.username ?? form.user.name}!</p>
	<p>Now you can <a href="/signin">sign in</a>.</p>
{:else}
	{#if form?.errors}
		<p>{form.errors}</p>
		<pre>{JSON.stringify(form, null, 2)}</pre>
	{/if}

	<form method="post" action="?/register">
		<input type="text" name="username" placeholder="Username" value={name} required />
		<input type="password" name="password" placeholder="Password" value="1" required />

		<button type="submit">Sign Up</button>
	</form>
{/if}

<script lang="ts">
	export let form;
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
		<input type="text" name="username" placeholder="Username" required />
		<input type="password" name="password" placeholder="Password" required />

		<button type="submit">Sign Up</button>
	</form>
{/if}

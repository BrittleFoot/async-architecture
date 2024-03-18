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
		<h3>Personal Information</h3>
		<input type="text" name="username" placeholder="Username" required />
		<input type="password" name="password" placeholder="Password" required />

		<h3>Beak Type</h3>
		<fieldset>
			<label for="admin">
				<input name="isAdmin" type="checkbox" />
				Admin
			</label>
			<label for="manager">
				<input name="isManager" type="checkbox" />
				Manager
			</label>

			<label for="performer">
				<input name="isPerformer" type="checkbox" checked />
				Performer
			</label>
		</fieldset>

		<button type="submit">Sign Up</button>
	</form>
{/if}

<style>
	fieldset {
		margin-bottom: 1em;
	}
</style>

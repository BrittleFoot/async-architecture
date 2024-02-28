<script lang="ts">
	import { page } from '$app/stores';

	let username = $page.data.user?.username ?? $page.data.session?.user?.name ?? 'User';
</script>

{#if $page.data.session}
<a href="/me">
	<button>{username}</button>
</a>
<a href="/signout">
	<button>Sign Out</button>
</a>
{:else}
<a href="/signup">
	<button>Sign Up</button>
</a>
<a href="/signin">
	<button class="success">Sign In</button>
</a>
{/if}

<style>
	button {
		border-radius: 2em;
		padding: 0.5em 0.6em;
		margin: -0.5em 0.1em;
	}
</style>
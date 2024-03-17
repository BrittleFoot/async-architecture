<script lang="ts">
	import { page } from '$app/stores';

	let username = $page.data.user?.username ?? $page.data.session?.user?.name ?? 'User';
</script>

<div class="nowrap">
	{#if $page.data.session}
		<li>
			<a href="/me">
				<button>{username}</button>
			</a>
		</li>
		<li>
			<a href="/signout">
				<button>Sign Out</button>
			</a>
		</li>
	{:else}
		<li>
			<a href="/signup">
				<button>Sign Up</button>
			</a>
		</li>
		<li>
			<a href="/signin">
				<button class="success">Sign In</button>
			</a>
		</li>
	{/if}
</div>

<style>
	button {
		border-radius: 2em;
		padding: 0.5em 0.6em;
		margin: -0.5em 0.1em;
	}

	.nowrap {
		white-space: nowrap;
		display: contents;
	}
</style>

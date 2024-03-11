<script>
	import { page } from '$app/stores';
	import SignInButtons from './SignInButtons.svelte';

	$: meAdmin = $page.data.user.roles.includes('admin');
</script>

<nav class="navbar">
	<img src="/parrots.webp" alt="parrot-bg" class="parrot-bg" />

	<ul>
		<li>
			<a href="/">
				<img src="/favicon.png" alt="parrot" class="parrot" />
			</a>
		</li>
	</ul>
	<ul>
		<li>
			<a href="/tracker">Tracker</a>
		</li>
		<li>
			<a href="/balance">Balance</a>
		</li>
		{#if meAdmin}
			<li>
				<a href="/analytics">Analytics</a>
			</li>
		{/if}
		<li>
			<SignInButtons />
		</li>
	</ul>
</nav>

<style>
	.parrot {
		width: 2em;
		height: 2em;
	}

	.navbar {
		position: relative;
		padding-left: 1em;
		padding-right: 1em;
	}

	.parrot-bg {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		width: 100%;
		object-fit: cover;
		opacity: 0.35;
		border-radius: 2em;
		z-index: -1;
	}
</style>

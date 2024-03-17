<script>
	import Logos from '$lib/components/Logos.svelte';
	import NavBar from '$lib/components/NavBar.svelte';
	import Sandbox from '$lib/components/Sandbox.svelte';
	import '../app.scss';
</script>

<div class="background">
	<img src="/space.webp" alt="background" />
</div>

<div id="root">
	<header>
		<NavBar />
	</header>

	<main class="container">
		<slot />
	</main>

	<footer>
		<Logos />
		<Sandbox />
	</footer>
</div>

<style>
	.background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		z-index: -999;
	}

	.background img {
		object-fit: cover;
		width: 100%;
		height: 100%;
		opacity: 0.5;
	}

	#root {
		display: grid;
		grid-row: auto;
		grid-template-rows: auto 1fr 8em;
		min-height: 100vh;
	}

	footer {
		position: relative;
		width: 100%;
		margin: 0 !important;
		padding: 0 !important;
	}

	main {
		margin-top: 0;
		margin-bottom: 0;
	}
</style>

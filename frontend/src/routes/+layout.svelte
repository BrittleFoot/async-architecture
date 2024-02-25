<script>
	import NavBar from '$lib/components/NavBar.svelte';
	import '../app.scss';
</script>

<div class="background">
	<img src="/space.webp" alt="background" />
</div>

<header>
	<NavBar />
</header>

<main class="container">
	<slot />
</main>

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
</style>

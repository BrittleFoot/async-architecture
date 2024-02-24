<script>
	import NavBar from '$lib/components/NavBar.svelte';
	import '../app.scss';
</script>

<header>
	<NavBar />
</header>

<main class="container">
	<slot />
</main>

<script lang="ts">
	import { onMount } from 'svelte';

	export let height: number;

	let cage: HTMLDivElement;

	onMount(() => {
		let randHeight = Math.floor(Math.random() * height);
		cage.style.top = `calc(${randHeight}px / 2)`;
		cage.style.zIndex = `-${height - randHeight}`;
	});
</script>

<div bind:this={cage}>
	<slot />
</div>

<style>
	div {
		position: absolute;
	}
</style>

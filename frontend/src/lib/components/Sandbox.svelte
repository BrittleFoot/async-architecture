<script lang="ts">
	import { onMount } from 'svelte';
	import WalkingBird from './WalkingBird.svelte';
	import Cage from './Cage.svelte';

	interface BirdParams {
		type: number;
		width: number;
		speedModifier: number;
		forward: boolean;
		delay: number;
		position: number;
	}

	let birds: BirdParams[] = [];
	let sandbox: HTMLDivElement;
	let containerHeight: number;
	let containerWidth: number;

	function randomInt(min: number, max: number) {
		return Math.floor(Math.random() * (max - min + 1) + min);
	}

	onMount(() => {
		containerWidth = sandbox.clientWidth;
		containerHeight = sandbox.clientHeight;

		console.log(containerWidth, containerHeight);

		let birdTypes = 4;
		let birdCount = randomInt(5, 9);

		for (let i = 0; i < birdCount; i++) {
			let width = randomInt(containerWidth / 2, containerWidth * 0.75);
			let position = randomInt(0, containerWidth - width);
			birds.push({
				type: randomInt(0, birdTypes - 1),
				width: width,
				position: position,
				speedModifier: (Math.random() - 0.5) / 2 + 1,
				forward: Math.random() > 0.5,
				delay: randomInt(0, 10000)
			});
		}

		birds = birds;
	});
</script>

<div class="sandbox" bind:this={sandbox}>
	{#each birds as bird, i}
		<Cage height={containerHeight}>
			<WalkingBird {...bird} />
		</Cage>
	{/each}
</div>

<style>
	.sandbox {
		position: relative;
		overflow: hidden;
		width: 100%;
		height: 100%;
		z-index: -50;
		margin: 0;
		padding: 0;
	}
</style>

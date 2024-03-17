<script lang="ts">
	import { onMount } from 'svelte';

	export let type = 0;
	export let width = 500;
	export let speedModifier = 1;
	export let forward = true;
	export let delay = 0;
	export let position = 0;

	$: src = `/walking/${type}.gif`;

	let parrot: HTMLImageElement;

	function walkAnimation(forward: boolean, width: number) {
		let start = forward ? position : position + width;
		let end = forward ? position + width : position;
		let dir = forward ? 1 : -1;

		return [
			{
				transform: `translateX(${start}px) scaleX(${dir})`,
				opacity: 0,
				offset: 0
			},
			{
				opacity: 1,
				offset: 0.1
			},
			{
				opacity: 1,
				offset: 0.9
			},
			{
				transform: `translateX(${end}px) scaleX(${dir})`,
				opacity: 0,
				offset: 1
			}
		];
	}

	onMount(() => {
		let baseSpeed = 50 * speedModifier; // 100 px per second base
		let rawDuration = width / baseSpeed;
		let duration = rawDuration;

		let anim = parrot.animate(walkAnimation(forward, width), {
			duration: duration * 1000,
			iterations: Infinity,
			delay: delay
		});

		parrot.style.filter = `hue-rotate(${Math.random() * 360}deg)`;

		return () => {
			anim.cancel();
		};
	});
</script>

<img bind:this={parrot} {src} alt="🦜" />

<style>
	img {
		height: 3em;
		aspect-ratio: preserve;
		top: 0;
		left: 0;
		opacity: 0;
	}
</style>

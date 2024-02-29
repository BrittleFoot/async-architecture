<script lang="ts">
	export let value: string;
	export let onClick: () => Promise<void>;

	let disabled = false;
	let busy: true | null = null;
	let error: any = null;

	async function handleClick(event: MouseEvent) {
		if (disabled) return;
		disabled = true;
		busy = true;
		try {
			await onClick();
		} catch (e) {
			console.log(e);
			error = e;
		} finally {
			disabled = false;
			busy = null;
		}
	}
</script>

<button on:click={handleClick} aria-busy={busy} {disabled}
	>{error ? error?.body?.message : value}</button
>

<style>
	button {
		width: 100%;
	}
</style>

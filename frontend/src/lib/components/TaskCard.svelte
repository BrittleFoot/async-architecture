<script lang="ts">
	import type { Task } from '$lib/api/tracker';
	import { slide } from 'svelte/transition';

	export let onMarkedCompleted: (task: Task) => Promise<void>;
	export let task: Task;
	let error: boolean | null = null;
	let disabled = false;

	async function handleSubmit() {
		disabled = true;
		// optimistic update!
		let prevTaskStatus = task.status;
		try {
			task.status = 'done';
			task = task;
			await onMarkedCompleted(task);
			error = null;
		} catch (error) {
			task.status = prevTaskStatus;
			task = task;
			error = true;
		}
		disabled = false;
	}
</script>

<form transition:slide on:submit|preventDefault={handleSubmit}>
	<input type="hidden" name="id" value={task.id} />
	<fieldset role="group">
		<input type="text" readonly value={task.summary} aria-label="Read-only input" />
		<input
			type="performer"
			readonly
			value="🦜 {task.performer?.username}"
			class="performer"
			aria-label="Read-only input"
		/>

		{#if task.status === 'done'}
			<button type="submit" class="nowrap success" disabled>Done 👍</button>
		{:else}
			<button type="submit" class="nowrap" {disabled}>Resolve</button>
		{/if}
	</fieldset>
</form>

<style>
	.performer {
		max-width: 10em;
		text-overflow: ellipsis;
		text-align: center;
	}

	.nowrap {
		white-space: nowrap;
		width: 11em;
	}
</style>

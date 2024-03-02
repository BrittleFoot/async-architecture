<script lang="ts">
	import { page } from '$app/stores';
	import type { Task } from '$lib/api/tracker';
	import { getErrorMsg } from '$lib/typeUtils';

	export let onMarkedCompleted: (task: Task) => Promise<void>;
	export let task: Task;
	let error: string | null = null;
	let submitting = false;

	$: isMeTaskOwner = task.performer?.publicId === $page.data.user?.publicId;

	$: disabled = !isMeTaskOwner || submitting;

	async function handleSubmit() {
		submitting = true;
		// optimistic update!
		let prevTaskStatus = task.status;
		try {
			task.status = 'done';
			task = task;
			await onMarkedCompleted(task);
			error = null;
		} catch (e) {
			task.status = prevTaskStatus;
			task = task;

			error = getErrorMsg(e);
		}
		submitting = false;
	}

</script>

<form on:submit|preventDefault={handleSubmit} class:optimistic={task.optimistic}>
	<input type="hidden" name="id" value={task.id} />
	<fieldset role="group">
		<input type="text" readonly value={task.summary} aria-label="Read-only input"/>
		<input type="text" class="divider" readonly value="🦜" aria-label="Read-only input" />
		<input
			type="performer"
			readonly
			value="{task.performer?.username ?? 'Unassigned'}"
			class="performer"
			aria-label="Read-only input"
		/>

		{#if error}
			<button type="submit" class="nowrap" {disabled}>
				😥
				<div class="tooltip" data-tooltip="{error}" data-placement="left"/>
			</button>
		{:else if task.status === 'done'}
			<button type="submit" class="nowrap success" disabled aria-busy={submitting}>
				{submitting ? "" : '👍'}
				<div class="tooltip" data-tooltip="Completed!"/>
			</button>
		{:else if isMeTaskOwner}
			<button type="submit" class="nowrap" {disabled} data-tooltip="Complete the task!">🏁</button>
		{:else}
			<button type="submit" class="nowrap secondary" disabled>
				🙊
				<div class="tooltip" data-tooltip="Not your task 🥳"/>
			</button>
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
		width: 8em;
	}

	.divider {
		width: 3em;
	}

	.tooltip {
		position: absolute;
		display: inline-block;
		top: 0;
		left: 0;
		margin: 0;
		padding: 0;
		width: 100%;
		height: 100%;
		border-bottom: 0;
		z-index: 10;
	}

	button {
		position: relative;
		pointer-events: all;
	}

	.optimistic {
		opacity: 0.5;
	}

</style>

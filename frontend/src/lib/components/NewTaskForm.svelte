<script lang="ts">
	import { faker } from '@faker-js/faker';
	import { onMount } from 'svelte';

	function capitalize(string: string) {
		return string.charAt(0).toUpperCase() + string.slice(1);
	}

	function suggestTask() {
		return (
			capitalize(faker.company.buzzVerb()) + ' a ' + faker.company.catchPhrase().toLowerCase() + '!'
		);
	}

	function suggestId() {
		let noun = faker.company.buzzNoun()
		while (noun.length > 9) {
			noun = faker.company.buzzNoun()
		}
		return noun.toUpperCase() + '-' + faker.number.int({ min: 1, max: 999 });
	}

	export let onTaskCreated: (taskId: string, summary: string) => Promise<void>;
	let summary = "";
	let taskId = "";
	let inputError: boolean | null = null;
	let disabled = false;
	$: text = disabled ? 'Creating' : 'Create a Task';

	onMount(() => {
		summary = suggestTask();
		taskId = suggestId();
	});

	async function handleSubmit(event: Event) {
		disabled = true;
		if (summary === '') {
			inputError = true;
			return;
		}
		try {
			await onTaskCreated(taskId, summary);
			inputError = null;
		} catch (error) {
			inputError = true;
		}
		summary = suggestTask();
		taskId = suggestId();
		disabled = false;
	}
</script>

<form on:submit|preventDefault={handleSubmit}>
	<fieldset role="group">
		<input
			class="task-id-input"
			type="text"
			name="taskId"
			placeholder="POPUG-1"
			required
			bind:value={taskId}
			aria-invalid={inputError}
		/>
		<input
			type="text"
			name="summary"
			placeholder="Do a flip!"
			required
			bind:value={summary}
			aria-invalid={inputError}
		/>
		<input type="submit" {disabled} aria-busy={disabled} value={text} />
	</fieldset>
</form>

<style>
	.task-id-input {
		width: 10rem;
		text-align: center;
	}
</style>
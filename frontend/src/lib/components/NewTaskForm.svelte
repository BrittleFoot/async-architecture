<script lang="ts">
	export let onTaskCreated: (summary: string) => Promise<void>;
	let summary = '';
	let inputError: boolean | null = null;
	let disabled = false;
	$: text = disabled ? 'Creating' : 'Create a Task';

	async function handleSubmit(event: Event) {
		disabled = true;
		if (summary === '') {
			inputError = true;
			return;
		}
		try {
			await onTaskCreated(summary);
			inputError = null;
		} catch (error) {
			inputError = true;
		}
		summary = '';
		disabled = false;
	}
</script>

<form on:submit|preventDefault={handleSubmit}>
	<fieldset role="group">
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

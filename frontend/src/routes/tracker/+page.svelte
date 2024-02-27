<script lang="ts">
	import { onMount } from 'svelte';
	import { TrackerService, type Task } from '$lib/api/tracker';
	import TaskCard from '$lib/components/TaskCard.svelte';
	import NewTaskForm from '$lib/components/NewTaskForm.svelte';

	let trackerService = new TrackerService(/*data.accessToken*/);
	let tasks: Task[] = [];
	let firstLoad = true;
	let hideCompleted = false;

	onMount(async () => {
		await refreshTasks();
		firstLoad = false;
	});

	async function completeTask(task: Task) {
		await trackerService.completeTask(task);
		await refreshTasks();
	}

	async function createTask(summary: string) {
		await trackerService.createTask(summary);
		await refreshTasks();
	}

	async function refreshTasks() {
		tasks = await trackerService.getTasks(hideCompleted);
	}
</script>

<h1>💻 Tracker</h1>

<h2>Become a Leader!</h2>

<NewTaskForm onTaskCreated={createTask} />

<div class="onliner">
	<h2>Tasks</h2>
	<label>
		Hide completed
		<input type="checkbox" bind:checked={hideCompleted} on:change={refreshTasks} />
	</label>
</div>

<div aria-busy={firstLoad} class="loader"></div>

{#each tasks as task (task.id)}
	<TaskCard {task} onMarkedCompleted={completeTask} />
{/each}

<style>
	.loader {
		position: absolute;
		top: 50%;
		left: 50%;
	}

	.onliner {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
	}
</style>

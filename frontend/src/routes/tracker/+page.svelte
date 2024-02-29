<script lang="ts">
	import { onMount } from 'svelte';
	import { TrackerService, type Task } from '$lib/api/tracker';
	import TaskCard from '$lib/components/TaskCard.svelte';
	import NewTaskForm from '$lib/components/NewTaskForm.svelte';
	import Button from '$lib/components/Button.svelte';

	export let data;

	let trackerService = new TrackerService(data.accessToken);
	let tasks: Task[] = [];
	let renderTasks: Task[] = [];
	let lastFull: Task[] = [];

	let firstLoad = true;
	let hideCompleted = false;

	$: userCanReassgn = data.user?.roles.includes('manager') || data.user?.roles.includes('admin');

	async function refreshTasks() {
		tasks = await trackerService.getTasks(hideCompleted);
		renderTasks = tasks;
	}

	onMount(async () => {
		try {
			await refreshTasks();
		}
		finally {
			firstLoad = false;
		}
	});

	async function completeTask(task: Task) {
		await trackerService.completeTask(task);
		await refreshTasks();
	}

	async function createTask(summary: string) {
		// optimistic update!
		renderTasks = [{ summary } as Task, ...tasks];
		let newTask = await trackerService.createTask(summary);
		// twice optimistic update!
		renderTasks = [newTask, ...tasks];
		await refreshTasks();
	}

	async function hideCompletedTasks() {
		// optimistic update!
		if (hideCompleted) {
			lastFull = tasks;
			renderTasks = tasks.filter((task) => task.status !== 'done' || !hideCompleted);
		} else {
			renderTasks = lastFull;
		}
		await refreshTasks();
	}

	async function reassign() {
		await trackerService.reassignTasks();
		await refreshTasks();
	}
</script>

<h1>💻 Tracker</h1>

<h2>Become a Leader!</h2>

<NewTaskForm onTaskCreated={createTask} />

{#if userCanReassgn}
	<div>
		<h2>Become a Mischief!</h2>
		<Button value="😵‍💫 REASSIGN TASKS 😵‍💫" onClick={reassign} />
	</div>
{/if}

<br />
<div class="onliner relative">
	<h2 class="section">Tasks</h2>
	<label>
		<span>Hide completed</span>
		<input type="checkbox" bind:checked={hideCompleted} on:change={hideCompletedTasks} />
	</label>

	<div aria-busy={firstLoad} class="loader"></div>
</div>

{#each renderTasks as task (task.id)}
	<TaskCard {task} onMarkedCompleted={completeTask} />
{/each}

<style>
	.relative {
		position: relative;
	}

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

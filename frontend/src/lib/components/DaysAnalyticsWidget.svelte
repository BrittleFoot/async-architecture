<script lang="ts">
	import type { Day } from '$lib/api/analytics';
	import { onMount } from 'svelte';

	let plot: HTMLDivElement;
	export let days: Day[];
    let visible = false;

    function prepareData(days: Day[]) {
        const x = days.map(day => {
            let name = day.name.split(', ');
            if (name.length == 1) {
                return name[0];
            }
            return name[1] + ', ' + name[2];
        });
        const y = days.map(day => day.highestRewardTransaction?.task?.reward || 0);
        const text = days.map(day => {
            if (!day.highestRewardTransaction) return 'No tasks were completed today';
            const task = day.highestRewardTransaction.task;
            const user = day.highestRewardTransaction.user;
            return task ? `<b>Task:</b> ${task.summary}<br><b>Reward:</b> ${task.reward}<br><b>Completed by:</b> ${user?.username}` : 'No tasks';
        });
        return { x, y, text };
    }

	onMount(async () => {
		// @ts-ignore
		const Plotly = await import('plotly.js-dist-min');

		const data = [
			{
				...prepareData(days),
                type: 'scatter',
                mode: 'lines+markers',
			}
		];

		const layout = {
			title: 'Highest Task Price',
			xaxis: {
				title: 'Day',
			},
			yaxis: {
				title: 'Price',
                range: [-3, 43],
			},
			margin: {
				l: 80,
				r: 80,
				b: 70,
				t: 60,
			},
            font: {
                size: 12,
                color: '#ffffff',
                font: 'Segoe UI',
            },
            plot_bgcolor: "#1a202ccc",
            paper_bgcolor: "#1a202ccc",
            hoverlabel: {
                bgcolor: '#2a303ccc',
                bordercolor: '#a6a6a6cc',
                font: {
                    color: '#ffffff'
                }
            },
            transition: {
                duration: 120,
                easing: 'cubic-in-out'
            }
		};

		const extra = {
			displayModeBar: false,
			responsive: true
		};
        visible = true;
		Plotly.newPlot(plot, data, layout, extra);
	});
</script>

<div class="hidden" class:visible={visible} bind:this={plot} />

<style>
	div {
		width: 100%;
		height: 16em;
		border-radius: 0.5em;
        overflow: hidden;
		box-shadow: 0 0 0.5em 0.1em #000000aa;
	}

    .hidden {
        visibility: hidden;
    }

    .visible {
        animation: fade-in 0.1s ease-in;
        visibility: visible;
    }

    @keyframes fade-in {
        from {
            opacity: 0.5;
        }
        to {
            opacity: 1;
        }
    }
</style>

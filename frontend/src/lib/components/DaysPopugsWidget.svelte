<script lang="ts">
	import type { DayInfo, UserInfo } from '$lib/api/analytics';
	import { onMount } from 'svelte';

	let plot: HTMLDivElement;
	export let days: DayInfo[];
    let visible = false;

    function getUsers(days: DayInfo[]) {
        let nonunique = days.map(day => {
            return day.users;
        }).flat();

        let users = new Map();
        nonunique.forEach(user => {
            users.set(user.publicId, user);
        });
        return Array.from(users.values());
    }

    function prepareData(days: DayInfo[], user: UserInfo) {

        const y = days
            .map(day => day.users.filter(u => u.id === user.id))
            .map(users => {
                if (users.length === 0) {
                    // empty stub
                    return {
                        id: user.id,
                        username: user.username,
                        publicId: user.publicId,
                        todayBalance: 0,
                        totalExpense: 0,
                        totalProfit: 0,
                        transactions: []
                    } as UserInfo
                }
                return users;
            })
            .flat()
            .map(user => user.todayBalance);
        return { y };
    }

    function getCompanyBalance(days: DayInfo[]) {
        return days
            .map(day => -1 * day.users
                .map(user => user.todayBalance)
                .reduce((a, b) => a + b, 0)
            )
    }

	onMount(async () => {
		// @ts-ignore
		const Plotly = await import('plotly.js-dist-min');

        const users = getUsers(days);

        const commonX = days.map(day => {
            let name = day.name.split(', ');
            if (name.length == 1) {
                return name[0];
            }
            return name[1] + ', ' + name[2];
        });

		let data = users.map(user => {
            return {
                x: commonX,
                ...prepareData(days, user),
                type: 'bar',
                opacity: 0.8,
                name: user.username,
                marker: {
                    line: {
                        color: '#9a9a9a',
                        width: 1
                    }
                }
            };
        });

        data = [
            {
                x: commonX,
                y: getCompanyBalance(days),
                type: 'bar',
                name: 'Company Profit',
                marker: {
                    line: {
                        color: '#1a1a1a',
                        width: 1
                    }
                }
            } as any,
            ...data
        ]

		const layout = {
			title: 'Performers Balance',
			xaxis: {
				title: 'Day',
			},
			yaxis: {
				title: 'Balance',
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
            },
            bargap: 0.5,
            bargroupgap: 0.1
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

<script lang="ts">
	import { BillingService, type BillingCycle, type Day } from '$lib/api/billing';
	import UserBillingCycle from '$lib/components/UserBillingCycle.svelte';
	import Button from '$lib/components/Button.svelte';
	import Pyro from '$lib/components/Pyro.svelte';
	import { onMount } from 'svelte';

	export let data;

	const me = data.user;
	const meAdmin = me?.roles.includes('admin') ?? false;

	const billing = new BillingService(data.tokenInfo.accessToken);

	// Fetch one by one, for cpu instead of network performance's sake

	// let daysPromise: Promise<DayLight[]> = getDays();
	// $: dayValue = selectedDay && fetchDayInfo(selectedDay.id);
	// let selectedDay: DayLight | null = null;
	// $: dayValue = selectedDay && fetchDayInfo(selectedDay.id);

	// async function getDays() {
	// 	let days = await billing.getDays();
	// 	selectedDay = days[days.length - 1];
	// 	return days;
	// }

	// async function fetchDayInfo(id: number): Promise<Day> {
	// 	return await billing.getDay(id);
	// }

	let daysPromise: Promise<Day[]> = Promise.resolve([]);
	let selectedDay: Day | null = null;

	$: dayValue = selectedDay && getDayInfo(selectedDay);

	onMount(async () => {
		daysPromise = getDays();
	});

	async function getDayInfo(day: Day) {
		return day;
	}

	async function getDays() {
		let days = await billing.getFullDays();
		selectedDay = days[days.length - 1];
		return days;
	}

	function netBalance(billingCycle: BillingCycle) {
		let balance = 0;
		for (const transaction of billingCycle.transactions) {
			if (transaction.type !== 'payment' && transaction.type !== 'bad_luck') {
				balance -= parseInt(transaction.credit);
				balance += parseInt(transaction.debit);
			}
		}
		return balance;
	}

	function balanceIndicator(billingCycle: BillingCycle) {
		let net = netBalance(billingCycle);
		if (net === 0) return '🤷';
		return net >= 0 ? '🔥' : '🥶';
	}

	async function endDay() {
		await billing.endDay();
		daysPromise = getDays();
	}

	let pyroHidden = true;
	async function celebrate() {
		pyroHidden = false;
		await new Promise((resolve, reject) => {
			setTimeout(() => {
				pyroHidden = true;
				resolve(0);
			}, 3000);
		});
	}
</script>

<h1>Balance</h1>

{#await daysPromise}
	<select>
		<option selected aria-busy="true">Loading...</option>
	</select>
{:then days}
	<select bind:value={selectedDay}>
		{#each days as day (day.id)}
			<option value={day}>{day.name}</option>
		{/each}
	</select>
{:catch error}
	<pre aria-invalid="true">{error.message}</pre>
{/await}

{#await dayValue}
	<p aria-busy="true">Loading...</p>
{:then day}
	{#if day}
		{#if !meAdmin}
			<h2>
				<span>{balanceIndicator(day.billingCycles[0])}</span>
				<span>{day.billingCycles[0].user.username}</span>
				<small>
					<span>·</span>
					<b>{netBalance(day.billingCycles[0])}</b>
					<span> today balance · </span>
					<b>{day.billingCycles[0].user.balance}</b>
					<span> total</span>
				</small>
			</h2>
			<div class="single-balance">
				<UserBillingCycle billingCycle={day.billingCycles[0]} />
			</div>
		{:else}
			<h3>Company Profit</h3>
			<Button
				value={'🥳 ' + (day.profit ?? 'Imformation Unavailable') + ' 🥳'}
				onClick={celebrate}
			/>
			<Pyro hide={pyroHidden} />
			<p></p>
			<h3>Performers</h3>
			{#each day.billingCycles as billingCycle (billingCycle.publicId)}
				<details open={me?.publicId === billingCycle.user.publicId}>
					<summary>
						<span>{balanceIndicator(billingCycle)}</span>
						<span>{billingCycle.user.username}</span>
						<small>
							<span>·</span>
							<b>{netBalance(billingCycle)}</b>
							<span> today balance · </span>
							<b>{billingCycle.user.balance}</b>
							<span> total</span>
						</small>
					</summary>
					<UserBillingCycle {billingCycle} />
				</details>
			{/each}
		{/if}
	{/if}
{:catch error}
	<pre aria-invalid="true">{error.message}</pre>
{/await}

{#if meAdmin}
	<h2>Time Machine</h2>
	<Button onClick={endDay} value={'End Day'} />
{/if}

<style>
	details {
		border-radius: 6px;
		background-color: transparent;
		padding: 1em;
		border: 1px solid #99999933;
		background-image: linear-gradient(to bottom, #313f5bee 0%, #1c212ce9 2em);
	}

	.single-balance {
		border-radius: 6px;
		background-color: transparent;
		padding: 1em;
		border: 1px solid #99999933;
		background-image: linear-gradient(to bottom, #313f5bee 0%, #1c212ce9 2em);
	}
</style>

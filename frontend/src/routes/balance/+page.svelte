<script lang="ts">
	import { BillingService, type BillingCycle, type Day, type DayLight } from '$lib/api/billing';
	import UserBillingCycle from '$lib/components/UserBillingCycle.svelte';
	import Button from '$lib/components/Button.svelte';
	import Pyro from '$lib/components/Pyro.svelte';

	export let data;

	const me = data.user;
	const meAdmin = me?.roles.includes('admin') ?? false;

	const billing = new BillingService(data.tokenInfo.accessToken);

	let daysPromise: Promise<DayLight[]> = getDays();
	let selectedDay: DayLight | null = null;
	$: dayValue = selectedDay && fetchDayInfo(selectedDay.id);

	async function getDays() {
		let days = await billing.getDays();
		selectedDay = days[days.length - 1];
		return days;
	}

	async function fetchDayInfo(id: number): Promise<Day> {
		return await billing.getDay(id);
	}

	function netBalance(billingCycle: BillingCycle) {
		let balance = 0;
		for (const transaction of billingCycle.transactions) {
			if (transaction.type !== 'payment') {
				balance -= parseInt(transaction.credit);
				balance += parseInt(transaction.debit);
			}
		}
		return balance;
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
				<span>{netBalance(day.billingCycles[0]) >= 0 ? '🔥' : '🥶'}</span>
				<span>{day.billingCycles[0].user.username}, </span>
				<span>{netBalance(day.billingCycles[0])}</span>
			</h2>
			<div class="single-balance">
				<UserBillingCycle billingCycle={day.billingCycles[0]} />
			</div>
		{:else}
            <h3>Company Profit</h3>
            <Button value={"🥳 " + (day.profit ?? "Imformation Unavailable") + " 🥳"} onClick={celebrate}/>
            <Pyro hide={pyroHidden}/>
            <p></p>
			<h3>Performers</h3>
			{#each day.billingCycles as billingCycle (billingCycle.publicId)}
				<details open>
					<summary>
						<span>{netBalance(billingCycle) >= 0 ? '🔥' : '🥶'}</span>
						<span>{billingCycle.user.username}, </span>
						<span>{netBalance(billingCycle)}</span>
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

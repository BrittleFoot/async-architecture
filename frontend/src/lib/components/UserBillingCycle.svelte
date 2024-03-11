<script lang="ts">
	import type { BillingCycle } from '$lib/api/billing';

	export let billingCycle: BillingCycle;
	const transactions = billingCycle.transactions;
	const payments = billingCycle.payments;
</script>

<h3>Transactions</h3>
{#if transactions.length === 0}
	<p>No transactions</p>
{:else}
	<div class="undertable">
		<table class="striped">
			<thead>
				<tr>
					<th>Type</th>
					<th>Description</th>
					<th>Credit</th>
					<th>Debit</th>
				</tr>
			</thead>
			<tbody>
				{#each transactions as transaction (transaction.id)}
					<tr>
						<td>{transaction.type}</td>
						<td>{transaction.comment}</td>
						<td>{transaction.credit}</td>
						<td>{transaction.debit}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{/if}

<br />
<h3>Payments</h3>
{#if payments.length === 0}
	<p>No payments</p>
{:else}
	<ul>
		{#each payments as payment (payment.id)}
			<li>
				<td>{payment.amount}</td>
				<td>{payment.status}</td>
			</li>
		{/each}
	</ul>
{/if}

<style>
	.undertable {
		border-radius: 6px;
		overflow: hidden;
	}

	table {
		margin: 0;
	}
</style>

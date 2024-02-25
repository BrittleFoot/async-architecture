<script lang="ts">
	import { page } from '$app/stores';
</script>

<h1>Books Error</h1>

<h2>{$page.status}</h2>

{#if $page.error}
	<p>{$page.error.message}</p>

	<table>
		<thead>
			<tr>
				<th>Header Name</th>
				<th>Value</th>
			</tr>
		</thead>
		<tbody>
			{#each $page.error.data.headers as [key, value]}
				<tr>
					<td>{key}</td>
					<td>{value}</td>
				</tr>
			{/each}
		</tbody>
	</table>
{/if}

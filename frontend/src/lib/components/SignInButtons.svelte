<script lang="ts">
	import { page } from '$app/stores';
</script>

{#if $page.data.session}
	<strong>{$page.data.session.user?.name ?? 'User'}</strong>
	<a href="/signout">Sign Out</a>
{:else}
	<a href="/signin">Sign In</a>
{/if}

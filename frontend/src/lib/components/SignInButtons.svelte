<script lang="ts">
	import { page } from '$app/stores';
</script>

{#if $page.data.session}
	<a href="/me">
		<strong>{$page.data.session.user?.name ?? 'User'}</strong>
	</a>
	<a href="/signout">Sign Out</a>
{:else}
	<a href="/signin">Sign In</a>
	<a href="/signup">Sign Up</a>
{/if}

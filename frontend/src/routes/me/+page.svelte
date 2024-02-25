<script lang="ts">
	export let data;
	let user = data.session?.user;
</script>

<h1>🦜 Me</h1>

<div class="card">
	<h2>User</h2>
	<pre>{JSON.stringify(data.me, null, 2)}</pre>
	<h2>Session</h2>
	<pre>{JSON.stringify(user, null, 2)}</pre>
</div>

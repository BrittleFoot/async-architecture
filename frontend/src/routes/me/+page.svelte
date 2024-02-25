<script lang="ts">
    export let data;
    let user = data.session?.user;
</script>


<h1>Me</h1>

<div class="card">
    <pre>{JSON.stringify(user, null, 2)}</pre>
</div>
<script lang="ts">
	export let data;
</script>

<h1>📚 Books</h1>

<ol>
	{#each data.books as book}
		<li>
			<a href="books/{book.id}">{book.name}</a> by
			<a href="authors/{book.author.id}">{book.author.name}</a>
		</li>
	{/each}
</ol>

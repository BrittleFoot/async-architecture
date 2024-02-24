<script lang="ts">
    import { onMount } from 'svelte';
    import { BookService, type Book } from '$lib/api/books';
    export let data;

    let books: Book[] = [];
    let booksService = new BookService(data.accessToken);

    onMount(async () => {
        books = await booksService.getBooks();
    });

</script>

<h1> Books </h1>

<ol>
    {#each books as book}
        <li>
            <a href="books/{book.id}">{book.name}</a> by <a href="authors/{book.author.id}">{book.author.name}</a>
        </li>
    {/each}
</ol>
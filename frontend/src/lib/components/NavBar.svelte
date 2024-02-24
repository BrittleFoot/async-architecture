<script>
	import SignInButtons from "./SignInButtons.svelte";

</script>



<nav class="navbar">
    <img src='/parrots.webp' alt='parrot-bg' class='parrot-bg' />

    <ul>
        <li>
            <a href="/">
                <img src='/favicon.png' alt='parrot' class='parrot' />
            </a>
        </li>
    </ul>
    <ul>
        <li>
            <a href="/books">Books</a>
        </li>
        <li>
            <a href="/authors">Authors</a>
        </li>
        <li>
            <SignInButtons/>
        </li>
    </ul>


</nav>

<style>
    .parrot {
        width: 2em;
        height: 2em;
    }

    .navbar {
        position: relative;
        padding-left: 1em;
        padding-right: 1em;
    }

    .parrot-bg {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        object-fit: cover;
        opacity: 0.2;
        border-radius: 2em;
        z-index: -1;
    }

</style>
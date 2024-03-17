<script lang="ts">
	let autoplay = 1;
	let url = `https://www.youtube.com/embed/dQw4w9WgXcQ?si=STyKRyReBEiXyIFY&autoplay=${autoplay}`;
</script>

<div>
	<iframe
		width="560"
		height="315"
		src={url}
		title="You've been Rickroled!"
		frameborder="0"
		allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
		allowfullscreen
	></iframe>
</div>

<section>
	<h1>
		Congratulations! You've been <a href="https://en.wikipedia.org/wiki/Rickrolling">Rickrolled</a>!
		🎉
	</h1>

	<h2>Wellcome to the Internet!</h2>

	<h1>Now, Seriously</h1>

	<p>
		Glad to have you here! This is a tracker for our "Uber Popug" company's daily tasks. You can
		add, edit, and delete tasks. You can also mark them as done.
	</p>

	<p>
		First, you need to register in our system. Then you can sign in and start using the tracker.
	</p>

	<p>
		Tasks are assigned randomly to our team members. Tasks have price, you will be charged small
		amount for each task assign. But after task is done, you will be greatly rewarded!.
	</p>

	<p>You can check your balance and see the history of your transactions.</p>

	<p>Now, let's get started!</p>

	<p>
		<a href="/signup"><button>Sign Up</button></a>
		<a href="/signin"><button class="success">Sign In</button></a>
	</p>
</section>

<style>
	section {
		margin-top: 1em;
	}

	div {
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>

<script>
	import TweetView from "./TweetView.svelte";
	export let tweets = undefined;
</script>

<main class="scroll">
	{#if tweets === null}
		<p>Error fetching tweets</p>
	{:else if tweets === undefined}
		<p>loading...</p>
	{:else if tweets.length > 0}
		{#each tweets as tweet}
			<TweetView {tweet} />
		{/each}
	{/if}
</main>

<style>
	.scroll {
		margin: 3px;
		padding: 4px;
		height: 90vh;
		overflow-x: hidden;
		overflow-y: auto;
		text-align: justify;
	}
</style>

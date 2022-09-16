<script>
	import TweetView from "./TweetView.svelte";
	export let tweets = [];
</script>

<main>
	{#if tweets === null}
		<p>Error fetching tweets</p>
	{:else if tweets === undefined}
		<p>loading...</p>
	{:else if tweets.length > 0}
		{#each tweets as tweet}
			<TweetView tweet={tweet} />
		{/each}
	{/if}
</main>

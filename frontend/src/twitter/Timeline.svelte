<script>
	import TweetView from "./TweetView.svelte";
	export let tweets = [];
</script>

<main>
	{#each tweets as tweet}
		<TweetView {tweet} />
	{/each}
</main>

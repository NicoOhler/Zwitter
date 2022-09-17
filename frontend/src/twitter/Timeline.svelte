<script>
	import TweetView from "./TweetView.svelte";
	import { Plane } from "svelte-loading-spinners";
	export let tweets = undefined;
</script>

<main class="scroll">
	{#if tweets === null}
		<p>Error fetching tweets</p>
	{:else if tweets === undefined}
		<div class="center">
			<Plane size="60" color="#FF3E00" unit="px" duration=".8s" />
		</div>
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
	.center {
		margin-top: 4vh;
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>

<script>
	import Search from "svelte-search";
	import { search } from "../endpoints.js";

	export let placeholder = "Search Zwitter";

	let value = "";
	let hashtags = [];
	let users = [];
</script>

<Search
	hideLabel
	{placeholder}
	bind:value
	on:submit={async () => {
		let results = await search(value);
		hashtags = results.hashtags;
		users = results.users;
	}}
/>
<ul>
	{#each hashtags as hashtag}
		<li><a href="/hashtag/{hashtag}">#{hashtag}</a></li>
	{/each}
	{#each users as user}
		<li><a href="/user/{user}">@{user}</a></li>
	{/each}
</ul>

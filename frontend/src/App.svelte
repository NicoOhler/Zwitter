<!-- start with npm run dev -->
<script>
	import Timeline from "./twitter/Timeline.svelte";
	import { Tabs, TabList, TabPanel, Tab } from "./ui/tabs/tabs.js";
	import { getUserTimeline, getHomeTimeline, getProfile } from "./endpoints.js";
	import { onMount } from "svelte";

	let user = "aigner";
	let userTimelineTweets = [];
	let homeTimelineTweets = [];
	let profile = undefined;

	// load data from backend
	onMount(async () => {
		// todo simplify this
		// get all tweets in user timeline
		let userTimeline = await getUserTimeline(user);
		if (Array.isArray(userTimeline)) {
			userTimeline.forEach((tweet) => {
				userTimelineTweets.push(JSON.parse(tweet));
			});
		} else {
			console.log("Error fetching user timeline");
			console.log(userTimeline);
			userTimelineTweets = null;
		}

		// get all tweets in home timeline
		let homeTimeline = await getHomeTimeline();
		if (Array.isArray(homeTimeline))
			homeTimeline.forEach((tweet) => {
				homeTimelineTweets.push(JSON.parse(tweet));
			});
		else {
			console.log("Error fetching home timeline");
			console.log(homeTimeline);
			homeTimelineTweets = null;
		}

		// get profile data
		//const response3 = await getProfile();
		//profile = response3.json();
	});
</script>

<Tabs>
	<TabList>
		<Tab>Home</Tab>
		<Tab>User</Tab>
		<Tab>Profile</Tab>
	</TabList>

	<TabPanel>
		{#if homeTimelineTweets == null}
			Error fetching home timeline
		{:else if homeTimelineTweets.length > 0}
			<Timeline tweets={homeTimelineTweets} />
		{:else}
			<p>loading...</p>
		{/if}
	</TabPanel>

	<TabPanel>
		{#if userTimelineTweets == null}
			Error fetching user timeline
		{:else if userTimelineTweets.length > 0}
			<Timeline tweets={userTimelineTweets} />
		{:else}
			<p>loading...</p>
		{/if}
	</TabPanel>

	<TabPanel><h2>Profile</h2></TabPanel>
</Tabs>

<style>
</style>

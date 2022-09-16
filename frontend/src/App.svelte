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
		// get all tweets in user timeline
		const response = await getUserTimeline(user);
		let userTimeline = response.json();
		console.log(userTimeline);
		userTimeline.forEach((tweet) => {
			userTimelineTweets.push(tweet);
		});

		// get all tweets in home timeline
		const response2 = await getHomeTimeline(user);
		let homeTimeline = response2.json();
		homeTimeline.forEach((tweet) => {
			homeTimelineTweets.push(tweet);
		});

		// get profile data
		//const response3 = await getProfile();
		//profile = response3.json();
	});
</script>

<Tabs>
	<TabList>
		<Tab>Home</Tab>
		<Tab>Latest</Tab>
		<Tab>Profile</Tab>
	</TabList>

	<TabPanel>
		<Timeline tweets={userTimelineTweets} />
	</TabPanel>

	<TabPanel>
		<Timeline tweets={homeTimelineTweets} />
	</TabPanel>

	<TabPanel><h2>Profile</h2></TabPanel>
</Tabs>

<style>
</style>

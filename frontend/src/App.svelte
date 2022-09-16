<!-- start with npm run dev -->
<script>
	import Timeline from "./twitter/Timeline.svelte";
	import { Tabs, TabList, TabPanel, Tab } from "./ui/tabs/tabs.js";
	import { getUserTimeline, getHomeTimeline, getProfile } from "./endpoints.js";
	import { onMount } from "svelte";

	let user = "aigner";
	let userTimeline = undefined;
	let homeTimeline = undefined;
	let profile = undefined;

	// load data from backend
	onMount(async () => {
		// todo simplify this
		// get all tweets in user timeline
		userTimeline = await getUserTimeline(user);

		// get all tweets in home timeline
		homeTimeline = await getHomeTimeline(user);

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
		<Timeline tweets={homeTimeline} />
	</TabPanel>

	<TabPanel>
		<Timeline tweets={userTimeline} />
	</TabPanel>

	<TabPanel><h2>Profile</h2></TabPanel>
</Tabs>

<style>
</style>

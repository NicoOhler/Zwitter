<!-- start with npm run dev -->
<script>
	import Timeline from "./twitter/Timeline.svelte";
	import SearchBar from "./twitter/SearchBar.svelte";
	import { Tabs, TabList, TabPanel, Tab } from "./ui/tabs/tabs.js";
	import SplitPane from "./ui/SplitPane.svelte";
	import { getUserTimeline, getHomeTimeline, getProfile } from "./endpoints.js";
	import { onMount } from "svelte";

	import logo from "../assets/logo/logo.png";

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

<SplitPane allowResize={false} leftInitialSize="15%">
	<svelte:fragment slot="left">
		<div class="center">
			<img src={logo} alt="logo" width="80vw" />
		</div>
	</svelte:fragment>
	<svelte:fragment slot="right">
		<SplitPane allowResize={false} leftInitialSize="75%">
			<svelte:fragment slot="left">
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
			</svelte:fragment>
			<svelte:fragment slot="right">
				<div class="center">
					<SearchBar />
				</div>
				<br />
				Discover<br />
				following<br />
				trending
			</svelte:fragment>
		</SplitPane>
	</svelte:fragment>
</SplitPane>

<style>
	.center {
		display: flex;
		justify-content: center;
		align-items: center;
	}
</style>

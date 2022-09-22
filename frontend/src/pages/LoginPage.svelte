<script>
	import { GoogleAuth } from "@beyonk/svelte-social-auth";
	import SplitPane from "../ui/SplitPane.svelte";
	import logo from "../../assets/logo/logo.png";

	let clientId = "692257273849-0oicl7ivddep930fh0v2dfrndqh5lbud.apps.googleusercontent.com";

	let handleLogin = (user) => {
		console.log(user);
	};

	let handleLoginFailure = (error) => {
		console.log(error);
	};
</script>

<SplitPane allowResize={false} leftInitialSize="15%">
	<svelte:fragment slot="left">
		<div class="center">
			<img src={logo} alt="logo" width="80vw" />
		</div>
	</svelte:fragment>
	<svelte:fragment slot="right">
		<h1>Join Zwitter today</h1>
		<GoogleAuth {clientId} on:auth-success={handleLogin} on:auth-failure={handleLoginFailure}>
			<button>Login with Google</button>
		</GoogleAuth>
	</svelte:fragment>
</SplitPane>

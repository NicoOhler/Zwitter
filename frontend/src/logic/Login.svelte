<script>
	const CLIENT_ID = "692257273849-0oicl7ivddep930fh0v2dfrndqh5lbud.apps.googleusercontent.com";
	export let logged_in = false;

	function onSignIn(googleUser) {
		// Useful data for your client-side scripts:
		var profile = googleUser.getBasicProfile();
		console.log("ID: " + profile.getId()); // Don't send this directly to your server!
		console.log("Name: " + profile.getName());
		console.log("Image URL: " + profile.getImageUrl());
		console.log("Email: " + profile.getEmail());

		// The ID token you need to pass to your backend:
		var id_token = googleUser.getAuthResponse().id_token;
		console.log("ID Token: " + id_token);

		logged_in = true;
	}
</script>

<svelte:head>
	<script src="https://accounts.google.com/gsi/client" async defer></script>
</svelte:head>

<br />Login {logged_in}
{#if !logged_in}
	<div id="g_id_onload" data-context="signin" data-client_id={CLIENT_ID} data-callback={onSignIn} data-auto_select="true" />
{/if}

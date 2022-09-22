<!-- start with npm run dev -->
<script>
	import MainPage from "./pages/MainPage.svelte";
	import LoginPage from "./pages/LoginPage.svelte";

	let logged_in = false;
</script>

{#if logged_in}
	<MainPage />
{:else}
	<LoginPage />
{/if}

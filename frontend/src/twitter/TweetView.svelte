<script>
	import Icon from "../ui/Icon.svelte";

	export let tweet;

	let created_at = new Date(tweet.created_at * 1000);
	// convert created_at to format of 3:45 PM - 1 Jan 2020
	created_at = created_at.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) + " - " + created_at.toLocaleDateString();
</script>

<div class="tweet">
	<svg viewBox="0 0 100 100" width={80} height={80}>
		<use href="#avatar" />
	</svg>
	<h1>{tweet.username}</h1>
	<h2>@{tweet.display_name}</h2>
	<h3>{created_at}</h3>
	<p>{tweet.content}</p>
	<div class="icons">
		<Icon href="like" />{tweet.like_count}
		<Icon href="reply" />{tweet.reply_count}
		<Icon href="retweet" />{tweet.retweet_count}
	</div>
</div>

<style>
	/* by default align the elements in the .tweet container */
	.tweet {
		margin: 1rem;
		padding: 1.25rem 1.75rem;
		border-radius: 5px;
		background: hsl(240, 20%, 15%);
		color: hsl(0, 0%, 100%);
		box-shadow: 0 1px 20px -10px hsla(0, 0%, 0%, 0.2);
		text-align: center;
	}
	/* by default separate the sibling elements starting with the second */
	.tweet > * + * {
		margin-top: 1rem;
	}
	.tweet h1 {
		font-size: 1.1rem;
	}
	.tweet h2,
	.tweet h3 {
		font-weight: 400;
		font-size: 1rem;
	}
	.tweet p {
		line-height: 2;
		font-size: 1.1rem;
		text-align: left;
		max-width: 350px;
	}
	/* display the icons in a vertically aligned row */
	.icons {
		color: hsl(40, 10%, 50%);
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	/* bonus: change the color of the text following a highlight
using the pseudo element on the entire document (`::selection {}`) would work as well
using the > direct children selector would skip the time element
*/
	.tweet *::selection {
		color: hsl(150, 95%, 40%);
	}

	/* when the viewport is wider than an arbitrary threshold */
	@media (min-width: 550px) {
		/* when grid is supported */
		@supports (display: grid) {
			/* remove the spacing introduced between the elements */
			.tweet > * + * {
				margin-top: initial;
			}
			.tweet {
				/* display the content in a grid with four columns and three rows */
				display: grid;
				gap: 1.25rem 1.5rem;
				grid-template-areas:
					"avatar handle name time"
					"avatar message message message"
					"avatar icons icons icons";
				/* reset the alignment of the nested elements */
				text-align: initial;
			}
			/* assign to each nested element the appropriate grid-area
        align the elements horizontally and vertically as needed
        */
			.tweet svg {
				grid-area: avatar;
				justify-self: center;
				align-self: center;
			}
			.tweet h1 {
				grid-area: name;
				align-self: baseline;
			}
			.tweet h2 {
				grid-area: handle;
				align-self: baseline;
			}
			.tweet h3 {
				grid-area: time;
				align-self: baseline;
				justify-self: end;
			}
			.tweet p {
				grid-area: message;
			}
			.tweet .icons {
				grid-area: icons;
			}
		}
	}
</style>

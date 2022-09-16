<!-- https://svelte.dev/repl/2fd524fb5c7f427891269b4d0928ac15?version=3.12.1 -->
<script>
    export let href;
    export let width = 25;
    export let height = 25;
</script>

<style>
    svg {
        display: block;
    }
</style>

<svg aria-hidden="true" viewBox="0 0 100 100" {width} {height}>
    <use href="#{href}" />
</svg>

<script>
  import { onMount } from 'svelte';
  import katex from 'katex';
  import 'katex/dist/katex.min.css';

  export let math = '';

  let renderedMath = '';

  // Function to render the LaTeX formula
  const renderMath = () => {
    try {
      renderedMath = katex.renderToString(math, {
        throwOnError: false,
        displayMode: true // Change to false for inline math
      });
    } catch (error) {
      renderedMath = `<span style="color: red;">Error rendering math</span>`;
    }
  };

  // Render when the component mounts
  onMount(renderMath);

  // Re-render whenever the `math` prop changes
  $: if (math) renderMath();
</script>

<div class="katex-container">
  {@html renderedMath}
</div>

<style>
  .katex-container {
    margin: 1em 0;
  }
</style>

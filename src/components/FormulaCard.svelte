<!-- src/FormulaCard.svelte -->
<script>
  import { fade } from 'svelte/transition';
  import Latex from '../components/Latex.svelte';
  
  export let formula;
  
  let showDescription = false;

  // Toggle description on click (mobile-friendly)
  function toggleDescription() {
    showDescription = !showDescription;
  }

  // Helper: create URL-friendly IDs.
  const slugify = str =>
    str
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^\w-]+/g, '');
</script>

<div
  id={slugify(formula.name)}
  class="border rounded-lg p-4 shadow hover:shadow-lg transition-shadow relative overflow-x-auto"
  on:click={toggleDescription}
  style="transition: all 200ms ease;"
>
  <a
    href={formula.link}
    target="_blank"
    rel="noopener noreferrer"
    class="text-lg w-fit font-semibold mb-2 block hover:underline"
  >
    {formula.name}
  </a>

  <Latex math={formula.formula} />

  {#if showDescription}
    <div transition:fade={{ duration: 200 }} class="mt-2 p-2 border rounded bg-gray-100 text-sm">
      {formula.description}
    </div>
  {/if}
</div>
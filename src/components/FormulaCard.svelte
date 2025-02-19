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
</script>

<div
  class="border rounded-lg p-4 shadow hover:shadow-lg transition-shadow relative cursor-pointer"
  on:mouseenter={() => showDescription = true}
  on:mouseleave={() => showDescription = false}
  on:click|stopPropagation={toggleDescription}
  style="transition: all 200ms ease;">
  <a
    href={formula.link}
    target="_blank"
    rel="noopener noreferrer"
    class="text-lg font-semibold mb-2 block hover:underline"
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

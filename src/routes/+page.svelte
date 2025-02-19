<!-- src/App.svelte -->
<script>
  import { onMount } from 'svelte';
  import FormulaCard from '../components/FormulaCard.svelte';
  import nestedCategories from './formulas.json';

  let showSidebar = false;

  // Helper: create URL-friendly IDs.
  const slugify = str =>
    str
      .toLowerCase()
      .replace(/\s+/g, '-')
      .replace(/[^\w-]+/g, '');

  // Optional: close sidebar when pressing Escape
  const handleKeydown = (event) => {
    if (event.key === 'Escape') {
      showSidebar = false;
    }
  };

  onMount(() => {
    window.addEventListener('keydown', handleKeydown);
    return () => window.removeEventListener('keydown', handleKeydown);
  });
</script>

<div class="flex">
  <!-- Desktop Sidebar -->
  <aside class="hidden md:block w-64 p-4 border-r border-gray-300 sticky top-0 h-screen overflow-y-auto">
    <h2 class="text-xl font-bold mb-4">Contents</h2>
    <ul class="space-y-2">
      {#each Object.entries(nestedCategories) as [category, subcategories]}
        <li>
          <a class="text-blue-600 hover:underline" href={`#${slugify(category)}`}>
            {category}
          </a>
          <ul class="ml-4 mt-1 space-y-1">
            {#each Object.entries(subcategories) as [subcategory, formulas]}
              <li>
                <a class="text-blue-500 hover:underline" href={`#${slugify(category)}-${slugify(subcategory)}`}>
                  {subcategory}
                </a>
              </li>
            {/each}
          </ul>
        </li>
      {/each}
    </ul>
  </aside>

  <!-- Main content container -->
  <div class="flex-1 relative">
    <!-- Mobile Header -->
    <header class="md:hidden fixed top-0 left-0 right-0 bg-white shadow z-20 flex items-center p-4">
      <button on:click={() => showSidebar = true} class="text-gray-700 focus:outline-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      <h1 class="flex-1 text-center text-xl font-bold">Nikolai's Formula Sheet</h1>
    </header>

    <!-- Mobile Sidebar Overlay -->
    {#if showSidebar}
      <div class="fixed inset-0 z-30 flex">
        <div class="fixed inset-0 bg-black opacity-50" on:click={() => showSidebar = false}></div>
        <aside class="relative w-64 bg-white shadow p-4 overflow-y-auto">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-bold">Contents</h2>
            <button on:click={() => showSidebar = false} class="text-gray-700 focus:outline-none">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <ul class="space-y-2">
            {#each Object.entries(nestedCategories) as [category, subcategories]}
              <li>
                <a class="text-blue-600 hover:underline" href={`#${slugify(category)}`} on:click={() => showSidebar = false}>
                  {category}
                </a>
                <ul class="ml-4 mt-1 space-y-1">
                  {#each Object.entries(subcategories) as [subcategory, formulas]}
                    <li>
                      <a class="text-blue-500 hover:underline" href={`#${slugify(category)}-${slugify(subcategory)}`} on:click={() => showSidebar = false}>
                        {subcategory}
                      </a>
                    </li>
                  {/each}
                </ul>
              </li>
            {/each}
          </ul>
        </aside>
      </div>
    {/if}

    <!-- Main Content -->
    <main class="p-4 max-w-6xl mx-auto pt-20 md:pt-4">
      <div class="hidden md:block">
        <div class="bg-blue-500 text-white p-4 rounded-lg mb-8 flex justify-center">
          <h1 class="text-3xl font-bold drop-shadow-lg text-center">Nikolai's Formula Sheet</h1>
        </div>

      </div>

      <!-- Loop over top-level categories -->
      {#each Object.entries(nestedCategories) as [category, subcategories]}
        <section id={slugify(category)} class="mb-12">
          <h2 class="flex justify-center text-2xl font-semibold mb-4">{category}</h2>
          
          <!-- Loop over subcategories within each top-level category -->
          {#each Object.entries(subcategories) as [subcategory, formulas]}
            <div class="mb-8">
              <h3 id={`${slugify(category)}-${slugify(subcategory)}`} class="text-xl font-semibold mb-2 ml-2 border-l-4 border-blue-500 pl-2">
                {subcategory}
              </h3>
              <!-- Add animate:flip to this grid container -->
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {#each formulas as formula (formula.id)}
                  <FormulaCard {formula} />
                {/each}
              </div>
            </div>
          {/each}
        </section>
        <hr class="p-4">
      {/each}
    </main>
  </div>
</div>

<style>
  main {
    min-height: 100vh;
  }
  @media (max-width: 767px) {
    main {
      padding-top: 4rem; /* Adjust based on your mobile header height */
    }
  }
</style>

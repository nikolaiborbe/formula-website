<!-- src/App.svelte -->
<script>
	import { onMount } from 'svelte';
	import FormulaCard from '../components/FormulaCard.svelte';
	import SearchModal from '../components/SearchModal.svelte';
	import nestedCategories from './formulas.json';
	import Credits from '../components/Credits.svelte';

	let showSidebar = false;
	let showSearch = false;

	// Helper: create URL-friendly IDs.
	const slugify = (str) =>
		str
			.toLowerCase()
			.replace(/\s+/g, '-')
			.replace(/[^\w-]+/g, '');

	// Close sidebar on Escape.
	const handleKeydown = (event) => {
		if (event.key === 'Escape') {
			showSidebar = false;
		}
	};

	// Open search modal on Ctrl+K or Cmd+K.
	const handleGlobalKeydown = (event) => {
		if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
			event.preventDefault();
			showSearch = true;
		}
	};

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);
		window.addEventListener('keydown', handleGlobalKeydown);

		return () => {
			window.removeEventListener('keydown', handleKeydown);
			window.removeEventListener('keydown', handleGlobalKeydown);
		};
	});
</script>

<div class="flex">
	<!-- Desktop Sidebar (md:block) -->
	<aside
		class="relative sticky top-0 hidden h-screen w-64 overflow-y-auto border-r border-gray-300 p-4 md:block"
	>
		<!-- Header row in the sidebar -->
		<div class="mb-4 flex items-center justify-between">
			<h2 class="text-xl font-bold">Contents</h2>
			<!-- Search button to toggle SearchModal -->
			<button
				class="flex cursor-pointer items-center
						 space-x-2 rounded-md border
						 border-gray-300 px-3
						 py-2 text-sm
						 text-gray-700
						 transition hover:bg-gray-100 focus:ring-2
						 focus:ring-blue-500 focus:outline-none"
				on:click={() => (showSearch = true)}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-4 w-4 text-gray-500"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M11 4a7 7 0 015.196 11.938l4.133 4.133a1 1 0 01-1.414 1.414l-4.133-4.133A7 7 0 1111 4z"
					/>
				</svg>
				<span class="font-medium">⌘K</span>
			</button>
		</div>

		<!-- List of categories -->
		<ul class="space-y-2">
			{#each Object.entries(nestedCategories) as [category, subcategories]}
				<li>
					<a class="text-blue-600 hover:underline" href={`#${slugify(category)}`}>
						{category}
					</a>
					<ul class="mt-1 ml-4 space-y-1">
						{#each Object.entries(subcategories) as [subcategory, formulas]}
							<li>
								<a
									class="text-blue-500 hover:underline"
									href={`#${slugify(category)}-${slugify(subcategory)}`}
								>
									{subcategory}
								</a>
							</li>
						{/each}
					</ul>
				</li>
			{/each}
		</ul>

		<!-- Custom div locked to the bottom left -->
		<div class="absolute bottom-0 left-0 w-full">
			<!-- Customize this content as needed -->
      <Credits />
		</div>
	</aside>

	<!-- Main Content Area -->
	<div class="relative flex-1">
		<!-- Mobile header (shows only on small screens) -->
		<header class="fixed top-0 right-0 left-0 z-20 flex items-center bg-white p-4 shadow md:hidden">
			<!-- Button to open mobile sidebar -->
			<button on:click={() => (showSidebar = true)} class="text-gray-700 focus:outline-none">
				<svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
				</svg>
			</button>
			<h1 class="flex-1 text-center text-xl font-bold">Nikolai's Formula Sheet</h1>
		</header>

		<!-- Mobile sidebar overlay -->
		{#if showSidebar}
			<div class="fixed inset-0 z-30 flex">
				<!-- Overlay background -->
				<div class="fixed inset-0 bg-black opacity-50" on:click={() => (showSidebar = false)}></div>

				<!-- Actual sidebar -->
				<aside class="relative w-64 overflow-y-auto bg-white p-4 shadow">
					<div class="mb-4 flex items-center justify-between">
						<h2 class="text-xl font-bold">Contents</h2>
						<div class="flex items-center space-x-2">
							<!-- Search button (mobile) -->
							<button
								class="flex items-center space-x-2
									 rounded-md border border-gray-300
									 px-4 py-2
									 text-sm text-gray-700
									 transition
									 hover:bg-gray-100 focus:ring-2 focus:ring-blue-500
									 focus:outline-none"
								on:click={() => {
									showSearch = true;
									showSidebar = false; // Optionally close sidebar when opening search
								}}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-4 w-4 text-gray-500"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
									stroke-width="2"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M11 4a7 7 0 015.196 11.938l4.133 4.133a1 1 0 01-1.414 1.414l-4.133-4.133A7 7 0 1111 4z"
									/>
								</svg>
							</button>

							<!-- Close sidebar button -->
							<button
								on:click={() => (showSidebar = false)}
								class="text-gray-700 focus:outline-none"
							>
								<svg
									class="h-6 w-6"
									fill="none"
									stroke="currentColor"
									stroke-width="2"
									viewBox="0 0 24 24"
								>
									<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
								</svg>
							</button>
						</div>
					</div>

					<ul class="space-y-2">
						{#each Object.entries(nestedCategories) as [category, subcategories]}
							<li>
								<a
									class="text-blue-600 hover:underline"
									href={`#${slugify(category)}`}
									on:click={() => (showSidebar = false)}
								>
									{category}
								</a>
								<ul class="mt-1 ml-4 space-y-1">
									{#each Object.entries(subcategories) as [subcategory, formulas]}
										<li>
											<a
												class="text-blue-500 hover:underline"
												href={`#${slugify(category)}-${slugify(subcategory)}`}
												on:click={() => (showSidebar = false)}
											>
												{subcategory}
											</a>
										</li>
									{/each}
								</ul>
							</li>
						{/each}
					</ul>

					<!-- Custom div locked to the bottom left for mobile sidebar -->
					<div class="absolute bottom-0 left-0 w-full">
						<!-- Customize this content as needed -->
             <Credits />
					</div>
				</aside>
			</div>
		{/if}

		<!-- Main content area -->
		<main class="mx-auto max-w-6xl p-4 pt-20 md:pt-4">
			<!-- Large screen header (hidden on mobile) -->
			<div class="hidden md:block">
				<div class="mb-8 flex justify-center rounded-lg bg-blue-500 p-4 text-white">
					<h1 class="text-center text-3xl font-bold drop-shadow-lg">Nikolai's Formula Sheet</h1>
				</div>
			</div>

			<!-- Sections of formulas -->
			{#each Object.entries(nestedCategories) as [category, subcategories]}
				<section id={slugify(category)} class="mb-12">
					<h2 class="mb-4 flex justify-center text-2xl font-semibold">{category}</h2>

					{#each Object.entries(subcategories) as [subcategory, formulas]}
						<div class="mb-8">
							<h3
								id={`${slugify(category)}-${slugify(subcategory)}`}
								class="mb-2 ml-2 border-l-4 border-blue-500 pl-2 text-xl font-semibold"
							>
								{subcategory}
							</h3>
							<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
								{#each formulas as formula (formula.id)}
									<FormulaCard {formula} />
								{/each}
							</div>
						</div>
					{/each}
				</section>
				<hr class="p-4" />
			{/each}
		</main>
	</div>
</div>

<!-- Search Modal (only visible when showSearch is true) -->
{#if showSearch}
	<SearchModal data={nestedCategories} onClose={() => (showSearch = false)} />
{/if}

<style>
	main {
		min-height: 100vh;
	}
	@media (max-width: 767px) {
		main {
			padding-top: 4rem;
		}
	}
</style>

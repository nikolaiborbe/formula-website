<!-- src/App.svelte -->
<script lang="ts">
	import RightContent from '../components/RightContent.svelte';
	import { onMount } from 'svelte';
	import FormulaCard from '../components/FormulaCard.svelte';
	import SearchModal from '../components/SearchModal.svelte';
	import nestedCategories from './formulas.json';
	import Sidebar from '../components/Sidebar.svelte';

	let showSidebar = false;
	let showSearch = false;

	// Helper: create URL-friendly IDs.
	const slugify = (str: string) =>
		str
			.toLowerCase()
			.replace(/\s+/g, '-')
			.replace(/[^\w-]+/g, '');

	// Close sidebar on Escape.
	const handleKeydown = (event: KeyboardEvent) => {
		if (event.key === 'Escape') {
			showSidebar = false;
		}
	};

	// Open search modal on Ctrl+K or Clg+K.
	const handleGlobalKeydown = (event: KeyboardEvent) => {
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

<div>
	<div class="flex">
		<!-- Sidebar component (handles both desktop and mobile views) -->
		<Sidebar
			{nestedCategories}
			{slugify}
			{showSidebar}
			onClose={() => (showSidebar = false)}
			onSearch={() => (showSearch = true)}
		/>

		<!-- Main Content Area -->
		<div class="relative mx-auto flex-1">
			<!-- Mobile header (shows only on small screens) -->
			<header
				class="fixed top-0 right-0 left-0 z-20 flex items-center bg-white p-4 shadow lg:hidden"
			>
				<!-- Button to open mobile sidebar -->
				<button
					aria-label="Mobile sidebar"
					on:click={() => (showSidebar = true)}
					class="text-gray-700 focus:outline-none"
				>
					<svg
						class="h-6 w-6"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						viewBox="0 0 24 24"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
					</svg>
				</button>
				<h1 class="flex-1 text-center text-xl font-bold">Nikolai's Formula Sheet</h1>
			</header>

			<!-- Main content area -->
			<main class="mx-auto max-w-6xl p-4 pt-20 lg:pt-4">
				<!-- Large screen header (hidden on mobile) -->
				<div class="hidden lg:block">
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
		<RightContent />
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

<!-- src/App.svelte -->
<script lang="ts">
	import RightContent from '../components/RightContent.svelte';
	import { onMount } from 'svelte';
	import { fade, scale } from 'svelte/transition';
	import FormulaCard from '../components/FormulaCard.svelte';
	import SearchModal from '../components/SearchModal.svelte';
	import nestedCategories from './formulas.json';
	import Sidebar from '../components/Sidebar.svelte';
	import LandingPage from '../components/LandingPage.svelte';

	let isMac = false;
	let morphed = false;

	onMount(() => {
		isMac = /Mac/.test(navigator.platform);
		setTimeout(() => {
			morphed = true;
		}, 2000);
	});

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
				class="fixed top-0 right-0 left-0 z-20 flex items-center justify-between bg-white px-3 shadow lg:hidden"
			>
				<!-- Button to open mobile sidebar -->
				<button
					aria-label="Mobile sidebar"
					on:click={() => (showSidebar = true)}
					class="px-3 py-5 text-gray-700 focus:outline-none"
				>
					<svg
						class="h-4 w-4"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						viewBox="0 0 24 24"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
					</svg>
				</button>

				{#if !morphed}
					<div in:fade={{ duration: 800 }}>
						<h1 in:scale={{ duration: 800 }} class="font-light">Nikolai's Formula Sheet</h1>
					</div>
				{:else}
					<div in:fade={{ duration: 800 }}>
						<a href="/">
							<img in:scale={{ duration: 800 }} src="favicon.png" alt="logo" class="h-8" />
						</a>
					</div>
				{/if}

				<button
					aria-label="Search"
					class="flex items-center rounded-lg px-3 py-5 text-sm text-gray-700 transition hover:bg-gray-100 focus:outline-none"
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
				</button>
			</header>

			<!-- Main content area -->
			<main class="mx-auto mt-4 max-w-6xl p-4 lg:pt-4">
				<!-- Large screen header (hidden on mobile) -->
				<LandingPage onSearch={() => (showSearch = true)}/>
				
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
	.intro {
		width: 200px; /* adjust as needed */
		height: 50px; /* adjust as needed */
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}
</style>

<script lang="ts">
  import { onMount } from 'svelte';
	import Credits from './Credits.svelte';
	export let nestedCategories: any;
	export let slugify: (str: string) => string;
	export let showSidebar: boolean;
	export let onClose: () => void;
	export let onSearch: () => void;

  let isMac = false;

  onMount(() => {
    isMac = /Mac/.test(navigator.platform);
  });
</script>

<!-- Desktop Sidebar (visible on medium screens and up) -->
<aside
	class="sticky top-0 hidden h-screen w-64  border-r border-gray-300 p-4 pb-0 lg:block "
>
	<!-- Header row in the sidebar -->
		<div class="mb-4 flex items-center justify-between">
			<h2 class="text-xl font-bold">Contents</h2>
			<!-- Search button to toggle SearchModal -->
			<button
				class="flex cursor-pointer items-center space-x-2 rounded-lg border border-gray-300 px-3 py-2 text-sm text-gray-700 transition hover:bg-gray-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
				on:click={onSearch}
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
				<span class="font-medium">{isMac ? '⌘K' : 'Ctrl+K'}</span>
			</button>
		</div>

		<!-- List of categories -->
	<div class="overflow-y-auto h-full pb-20">
		<ul class="space-y-4 mb-20">
			{#each Object.entries(nestedCategories) as [category, subcategories]}
				<li>
					<a class="category" href={'#' + slugify(category)}>
						{category}
					</a>
					<ul class="mt-3 space-y-3">
						{#each Object.entries(subcategories) as [subcategory, formulas]}
							<li class="subcategory cursor-pointer pl-4 hover:border-l-2">
								<a
									class="block h-full w-full"
									href={'#' + slugify(category) + '-' + slugify(subcategory)}
								>
									{subcategory}
								</a>
							</li>
						{/each}
					</ul>
				</li>
			{/each}
		</ul>
	</div>

	<footer class="absolute bottom-0 left-0 w-full bg-white p-4">
		<Credits />
	</footer>
</aside>

<!-- Mobile Sidebar (visible when showSidebar is true) -->
{#if showSidebar}
	<div class="fixed inset-0 z-30 flex">
		<!-- Overlay background -->
		<button
			type="button"
			class="fixed inset-0 bg-black opacity-50"
			aria-label="Close sidebar"
			on:click={onClose}
			on:keydown={(event) => event.key === 'Enter' && onClose()}
		></button>

		<!-- Actual sidebar -->
		<aside class="relative flex w-64 flex-col bg-white shadow">
			<!-- Header (stuck to the top) -->
			<header class="sticky top-0 z-10 bg-white p-4">
				<div class="flex items-center justify-between">
					<h2 class="text-xl font-bold">Contents</h2>
					<div class="flex items-center space-x-2">
						<!-- Search button (mobile) -->
						<button
							aria-label="Search"
							class="mr-4 flex items-center space-x-2 rounded-lg p-4 text-sm text-gray-700 transition hover:bg-gray-100 focus:outline-none"
							on:click={() => {
								onSearch();
								onClose(); // Optionally close sidebar when opening search
							}}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-5 w-5 text-gray-500"
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
							aria-label="Close sidebar"
							on:click={onClose}
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
			</header>

			<!-- Scrollable content -->
			<div class="flex-1 overflow-y-auto p-4">
				<ul class="space-y-7">
					{#each Object.entries(nestedCategories) as [category, subcategories]}
						<li>
							<a class=" category" href={'#' + slugify(category)} on:click={onClose}>
								{category}
							</a>
							<ul class="mt-4 space-y-5">
								{#each Object.entries(subcategories) as [subcategory, formulas]}
									<li class="pl-4">
										<a
											class="subcategory block h-full w-full"
											href={'#' + slugify(category) + '-' + slugify(subcategory)}
											on:click={onClose}
										>
											{subcategory}
										</a>
									</li>
								{/each}
							</ul>
						</li>
					{/each}
				</ul>
			</div>

			<!-- Footer (stuck to the bottom) -->
			<footer class="sticky bottom-0 z-10 bg-white p-4">
				<Credits />
			</footer>
		</aside>
	</div>
{/if}

<style>
	.category {
		font-size: 1rem;
		font-weight: 400;
	}
	.category:hover {
		font-weight: 500;
	}
	.subcategory {
		font-size: 0.9rem;
		font-weight: 400;
	}
	.subcategory:hover {
		font-weight: 500;
	}
</style>

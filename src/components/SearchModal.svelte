<!-- src/SearchModal.svelte -->
<script>
	import { onMount, onDestroy, afterUpdate } from 'svelte';

	// Data passed from parent – this should be your nested JSON of formulas.
	export let data = {};
	// Callback to signal the modal should be closed.
	export let onClose = () => {};

	let query = '';
	let results = [];
	let selectedIndex = 0;
	// Array to store references to each list item
	let resultItems = [];
	let inputEl;

	// A basic slugify helper for generating URL-friendly strings.
	const slugify = (str) =>
		str
			.toLowerCase()
			.replace(/\s+/g, '-')
			.replace(/[^\w-]+/g, '');

	// Run a search every time the query changes.
	$: results = query.trim() ? search(query) : [];
	// Reset the selectedIndex whenever new results come in.
	$: {
		if (results.length > 0) {
			selectedIndex = 0;
		}
	}

	// --- Fuzzy Matching Helpers ---

	// Computes the Levenshtein distance between two strings.
	function levenshtein(a, b) {
		const matrix = [];
		// increment along the first column of each row
		for (let i = 0; i <= b.length; i++) {
			matrix[i] = [i];
		}
		// increment each column in the first row
		for (let j = 0; j <= a.length; j++) {
			matrix[0][j] = j;
		}
		// Fill in the rest of the matrix
		for (let i = 1; i <= b.length; i++) {
			for (let j = 1; j <= a.length; j++) {
				if (b.charAt(i - 1) === a.charAt(j - 1)) {
					matrix[i][j] = matrix[i - 1][j - 1];
				} else {
					matrix[i][j] = Math.min(
						matrix[i - 1][j - 1] + 1, // substitution
						matrix[i][j - 1] + 1, // insertion
						matrix[i - 1][j] + 1 // deletion
					);
				}
			}
		}
		return matrix[b.length][a.length];
	}

	// Returns true if the token fuzzy matches any word in the field within the threshold.
	function fuzzyMatchInField(token, field, threshold = 2) {
		const words = field.split(/\s+/);
		for (const word of words) {
			if (levenshtein(token, word) <= threshold) {
				return true;
			}
		}
		return false;
	}

	// --- Updated Search Function with Fuzzy Matching ---
	function search(q) {
		const tokens = q
			.trim()
			.split(/\s+/)
			.map((token) => token.toLowerCase());
		let matches = [];
		for (const category in data) {
			const subcategories = data[category];
			for (const subcategory in subcategories) {
				const formulas = subcategories[subcategory];
				formulas.forEach((formula) => {
					const title = formula.name.toLowerCase();
					const description = formula.description.toLowerCase();
					const formulaText = formula.formula ? formula.formula.toLowerCase() : '';
					const link = formula.link ? formula.link.toLowerCase() : '';
					const searchTerms =
						formula.search_terms && Array.isArray(formula.search_terms)
							? formula.search_terms.map((term) => term.toLowerCase())
							: [];

					let score = 0;
					let allTokensFound = true;

					for (const token of tokens) {
						let tokenFound = false;

						// Exact matching first.
						if (title.includes(token)) {
							score += 10;
							tokenFound = true;
						} else if (searchTerms.some((term) => term.includes(token))) {
							score += 5;
							tokenFound = true;
						} else if (description.includes(token)) {
							score += 1;
							tokenFound = true;
						} else if (formulaText.includes(token)) {
							score += 1;
							tokenFound = true;
						} else if (link.includes(token)) {
							score += 1;
							tokenFound = true;
						}

						// Fuzzy matching if exact match wasn't found.
						if (!tokenFound) {
							if (fuzzyMatchInField(token, title)) {
								score += 10 * 0.5;
								tokenFound = true;
							} else if (searchTerms.some((term) => fuzzyMatchInField(token, term))) {
								score += 5 * 0.5;
								tokenFound = true;
							} else if (fuzzyMatchInField(token, description)) {
								score += 1 * 0.5;
								tokenFound = true;
							} else if (fuzzyMatchInField(token, formulaText)) {
								score += 1 * 0.5;
								tokenFound = true;
							} else if (fuzzyMatchInField(token, link)) {
								score += 1 * 0.5;
								tokenFound = true;
							}
						}

						if (!tokenFound) {
							allTokensFound = false;
							break;
						}
					}

					if (allTokensFound && score > 0) {
						matches.push({
							...formula,
							hash: slugify(formula.name),
							score
						});
					}
				});
			}
		}
		matches.sort((a, b) => b.score - a.score);
		return matches;
	}

	// Global keydown for Escape.
	function handleGlobalKeydown(event) {
		if (event.key === 'Escape') {
			onClose();
		}
	}

	let originalOverflow;
	onMount(() => {
		originalOverflow = document.body.style.overflow;
		document.body.style.overflow = 'hidden';
		window.addEventListener('keydown', handleGlobalKeydown);
		if (inputEl) {
			inputEl.focus();
			inputEl.select();
		}
	});

	onDestroy(() => {
		document.body.style.overflow = originalOverflow;
		window.removeEventListener('keydown', handleGlobalKeydown);
	});

	// Navigate the results with arrow keys and select with Enter.
	function handleInputKeydown(event) {
		if (event.key === 'ArrowDown') {
			if (selectedIndex < results.length - 1) {
				selectedIndex += 1;
			}
			event.preventDefault();
		} else if (event.key === 'ArrowUp') {
			if (selectedIndex > 0) {
				selectedIndex -= 1;
			}
			event.preventDefault();
		} else if (event.key === 'Enter') {
			if (results[selectedIndex]) {
				goToResult(results[selectedIndex]);
			}
			event.preventDefault();
		}
	}

	// When a result is clicked, navigate to it and close the modal.
	function goToResult(result) {
		const element = document.getElementById(result.hash);
		if (element) {
			element.scrollIntoView({ behavior: 'smooth', block: 'center' });
			element.classList.add('flash-highlight');
			setTimeout(() => {
				element.classList.remove('flash-highlight');
			}, 3000);
		} else {
			location.hash = result.hash;
		}
		onClose();
	}

	// After every update, scroll the selected item into view.
	afterUpdate(() => {
		if (resultItems[selectedIndex]) {
			resultItems[selectedIndex].scrollIntoView({
				behavior: 'smooth',
				block: 'nearest'
			});
		}
	});
</script>

<div
	class="fixed inset-0 z-50 flex items-start justify-center bg-black/5 pt-0 backdrop-blur-xs md:pt-56"
	on:click={onClose}
>
	<div class="w-[40rem] rounded-b-xl bg-white shadow-lg md:rounded-xl" on:click|stopPropagation>
		<div class="relative">
			<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
				<svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1116.65 6.65a7.5 7.5 0 010 10.5z"
					/>
				</svg>
			</div>
			<input
				type="text"
				bind:value={query}
				on:keydown={handleInputKeydown}
				placeholder="Search formulas..."
				class="w-full rounded p-4 pl-12 focus:outline-none"
				autofocus
				bind:this={inputEl}
			/>
		</div>
		{#if query.trim() && results.length === 0}
			<div>No results found.</div>
		{/if}
		{#if results.length > 0}
			<ul class="max-h-[30rem] overflow-y-auto md:max-h-96">
				{#each results as result, index}
					<li
						class="cursor-pointer p-4 last:border-0 hover:bg-gray-100"
						class:bg-gray-200={index === selectedIndex}
						on:click={() => goToResult(result)}
						bind:this={resultItems[index]}
					>
						<div class="font-bold">{result.name}</div>
						<div class="text-sm text-gray-500">{result.description}</div>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
</div>

<style>
	/* Additional styles if needed */
</style>

<script lang="ts">
	import { onMount } from 'svelte';
	import Latex from './Latex.svelte';
	import FormulaCard from './FormulaCard.svelte';
	export let onSearch: () => void;

	let formula = {
		id: 13,
		name: 'Lorentz Factor',
		formula: '\\gamma = \\frac{1}{\\sqrt{1-\\frac{v^2}{c^2}}}',
		link: 'https://en.wikipedia.org/wiki/Lorentz_factor',
		description: 'γ: Lorentz factor, v: velocity, c: speed of light',
		search_terms: ['γ', 'Lorentz factor', 'gamma', 'v', 'velocity', 'c', 'speed of light']
	};

	let formula2 = {
		id: 17,
		name: 'Heisenberg Uncertainty Principle',
		formula: '\\Delta x \\Delta p \\geq \\frac{\\hbar}{2}',
		link: 'https://en.wikipedia.org/wiki/Uncertainty_principle',
		description:
			"Δx: uncertainty in position, Δp: uncertainty in momentum, ħ: reduced Planck's constant",
		search_terms: [
			'Δx',
			'uncertainty in position',
			'position uncertainty',
			'Δp',
			'uncertainty in momentum',
			'momentum uncertainty',
			'ħ',
			"reduced Planck's constant",
			'Heisenberg Uncertainty Principle'
		]
	};

	// Replicate the slugify helper from FormulaCard for its element ID.
	function slugify(str: string): string {
		return str.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]+/g, '');
	}

	// Reactive state to toggle the underline for formula2.
	let underline = true;
	// Reactive flag for displaying the popup text on the second card.
	let showPopup = true;
	// Reactive flag for displaying the pointer popup on the first card.
	let showPointer = false;

	onMount(() => {
		// Simulate FormulaCard clicks every 3000ms (for the first card).
		const cardId = slugify(formula.name);
		const cardInterval = setInterval(() => {
			const el = document.getElementById(cardId);
			if (el) {
				el.click();
			}
		}, 4000);

		// Every 3000ms, toggle the underline and popup on the second card.
		const underlineInterval = setInterval(() => {
			underline = !underline;
			showPopup = !showPopup;
		}, 4000);

		// Every 3000ms, toggle the pointer popup on the first card.
		const pointerInterval = setInterval(() => {
			showPointer = !showPointer;
		}, 4000);

		return () => {
			clearInterval(cardInterval);
			clearInterval(underlineInterval);
			clearInterval(pointerInterval);
		};
	});
</script>

<style>
	/* Pointer style for the first FormulaCard */
	.pointer {
		position: absolute;
		top: -3rem; /* adjust as needed */
		left: 50%;
		transform: translateX(-50%);
		background: rgba(0, 0, 0, 0.8);
		color: #fff;
		font-size: 1rem;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		white-space: nowrap;
		z-index: 10;
		opacity: 0;
		transition: opacity 200ms ease;
	}
	.pointer.show {
		opacity: 1;
	}
	.pointer::after {
		content: "";
		position: absolute;
		top: 100%;
		left: 50%;
		transform: translateX(-50%);
		border-width: 5px;
		border-style: solid;
		border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
	}

	/* Styling for the popup box on the second card */
	.popup {
		position: absolute;
		top: -3rem; /* moved up slightly to make room for larger text */
		left: 50%;
		transform: translateX(-50%);
		background: rgba(0, 0, 0, 0.8);
		color: #fff;
		font-size: 1rem;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		white-space: nowrap;
		z-index: 10;
		opacity: 0;
		transition: opacity 200ms ease;
	}
	.popup.show {
		opacity: 1;
	}
	.popup::after {
		content: "";
		position: absolute;
		top: 100%;
		left: 50%;
		transform: translateX(-50%);
		border-width: 5px;
		border-style: solid;
		border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
	}
</style>

<div class="mt-10 mb-40 md:mb-50 md:mt-40">
	<div class="flex flex-col">
		<h1 class="text-4xl font-[480] md:text-8xl">
			Finding Formulas <span class="font-thin"> Made Easy</span>
		</h1>
    <p class="text-slate-600 text-xl md:text-2xl md:max-w-3/4 pt-5 font-light">Find formulas with named variables, <span class="text-sky-400">LaTeX</span>-rendered equations, and linked resources — all backed by a powerful <span class="text-sky-400 ">search</span> and sleek, modern design for effortless discovery.</p>
		<div class="mt-20 flex grid-cols-1 flex-wrap justify-center gap-4 self-center">
			<!-- First FormulaCard with pointer -->
			<div class="h-50 w-86 relative">
				<FormulaCard {formula} />
				<div class="pointer {showPointer ? 'show' : ''}">
					Click For Variable Names
				</div>
			</div>
			<!-- Second card remains unchanged except for its popup -->
			<div class="w-86 relative">
				<div
					class="relative overflow-x-auto rounded-lg border p-4 shadow transition-shadow hover:shadow-lg"
					style="transition: all 200ms ease;"
				>
					<a
						href={formula2.link}
						target="_blank"
						rel="noopener noreferrer"
						class="mb-2 block w-fit text-lg font-semibold {underline ? 'underline' : ''}"
					>
						{formula2.name}
					</a>
					<Latex math={formula2.formula} />
				</div>
				<!-- Popup text for the second card -->
				<div class="popup {showPopup ? 'show' : ''}">
					Read About Formulas
				</div>
			</div>
		</div>
		<button
			on:click={onSearch}
			class="button mt-14 w-40 cursor-pointer self-center rounded-xl border-2 p-2 shadow shadow-black transition hover:shadow-none"
		>
			Try the search
		</button>
	</div>
</div>

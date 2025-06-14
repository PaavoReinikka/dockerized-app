<script>
    import { readPriceRange } from '$lib/apis/data-api.js';
    import { onMount } from 'svelte';
	import { getTomorrow } from '$lib/utils/date-helpers.js';
    
    let data = $state(null); // Store the fetched prices
	const maxDate = getTomorrow();

    const start = new Date();
    start.setUTCHours(0, 0, 0, 0); // Set to midnight UTC

    const end = new Date(start);
    end.setUTCDate(end.getUTCDate() + 2); // Add 2 days

    function toZeroSecondsISOString(date) {
        const d = new Date(date);
        d.setUTCSeconds(0, 0);
        return d.toISOString().split('.')[0] + 'Z';
    }

    let dateRange = $state({
        startDate: toZeroSecondsISOString(start),
        endDate: toZeroSecondsISOString(end)
    });

	let currentPage = $state(1);
	const pricesPerPage = 20;

	let paginatedData = $derived.by(() => {
		if (!data || data.length === 0) return [];
		const start = (currentPage - 1) * pricesPerPage;
		return data.slice(start, start + pricesPerPage);
	});

	let totalPages = $derived.by(() => {
		if (!data) return 0;
		return Math.ceil(data.length / pricesPerPage);
	});

    async function fetchPrices() {
        try {
            const response = await readPriceRange(dateRange.startDate, dateRange.endDate);
            data = response;
			currentPage = 1;
        } catch (error) {
            console.error('Error fetching prices:', error);
        }
	}
	
</script>

<div class="flex flex-col justify-center items-center m-2">
	<h1>Choose days:</h1>

	<div class="flex gap-5 relative w-fit">
		<div class="flex flex-col">
			<p>Start</p>
			<input
				type="date"
				name="startDate"
				bind:value={dateRange.startDate}
				class="input preset-outlined-primary-500"
				max={maxDate}
			/>
		</div>
		<div class="flex flex-col">
			<p>End</p>
		<input
			type="date"
			name="endDate"
			bind:value={dateRange.endDate}
			class="input preset-outlined-primary-500"
			max={maxDate}
		/>
		</div>
	</div>
	<button class="btn preset-filled-primary-500 hover:preset-filled-primary-500 mt-2" id="submitDates" onclick={() => fetchPrices()}>Generate Table</button>

	{#if data && data.length > 0}
		<h2 class="text-xl font-semibold mb-4 text-center">Price Table</h2>
		<div class="overflow-x-auto">
			<table id="pricetable" class="min-w-full bg-white border border-gray-200 rounded-md shadow-sm mb-5">
				<thead class="bg-gray-300">
					<tr>
						<th class="text-left px-4 py-2 border-b text-primary-700">Date and Time</th>
						<th class="text-left px-4 py-2 border-b text-primary-700">Price (€/kWh)</th>
					</tr>
				</thead>
				<tbody>
					{#each paginatedData as { startDate, price }}
						<tr class="hover:bg-gray-50">
							<td class="px-4 py-2 border-b text-sm text-gray-700">
								{new Date(startDate).toLocaleString('fi-FI', {
									day: '2-digit',
									month: '2-digit',
									hour: '2-digit',
									minute: '2-digit'
								})}
							</td>
							<td class="px-4 py-2 border-b text-sm text-gray-700">{price.toFixed(3)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
			<div class="flex justify-center items-center gap-4 mt-4">
				<button
					disabled={currentPage === 1}
					onclick={() => currentPage--}
					class="px-4 py-2 btn rounded preset-filled-primary-500 hover:preset-filled-primary-500 disabled:opacity-50"
				>
					Previous
				</button>
				<p>Page {currentPage} of {totalPages}</p>
				<button
					disabled={currentPage === totalPages}
					onclick={() => currentPage++}
					class="px-4 py-2 btn rounded preset-filled-primary-500 hover:preset-filled-primary-500 disabled:opacity-50"
				>
					Next
				</button>
			</div>

		</div>
	{:else}
		<p class="text-gray-600">No data fetched yet.</p>
	{/if}
</div>

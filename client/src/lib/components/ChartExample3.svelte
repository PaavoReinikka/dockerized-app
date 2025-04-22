<script>
	import chartjs from 'chart.js/auto';
	import { onMount } from 'svelte';
	import { usePricesState } from '$lib/states/usePricesState.svelte';


	// THIS IS THE CHART EXAMPLE 3
	// here we are using the prices state to get the data for the chart
	// the state can be updated when needed (prices.update)
	let prices = usePricesState();
	let ctx;
	let chartCanvas;

	onMount(async (promise) => {
        // trick to force the stateful data into standard javascript object
		// this is a workaround for the fact that svelte stores are not serializable
		const chartData = prices.state2js();

		ctx = chartCanvas.getContext('2d');
		var chart = new chartjs(ctx, {
				type: chartData.chartType,
				data: {
						labels: chartData.chartLabels,
						datasets: [{
								label: undefined,
								backgroundColor: 'rgb(70, 50, 255)',
								borderColor: 'rgb(255, 255, 255)',
								data: chartData.chartValues,
						}]
				}
		});

	});
</script>

<canvas bind:this={chartCanvas} id="myChart" class="
	absolute
	bottom-10
	top-10
	m-auto
	rounded"
 style="width: 100%;background-color: #1e1e2f;"
></canvas>

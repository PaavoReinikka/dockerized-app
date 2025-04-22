<script>
	import chartjs from 'chart.js/auto';
	import { readData } from '$lib/apis/data-api.js';
	import { onMount } from 'svelte';

	
    let ctx;
	let chartCanvas;

    // onMount is a lifecycle function that runs when the component is mounted
    // it is similar to componentDidMount in React
	onMount(async (promise) => {
        // get the data from the API
        const data = await readData();
		ctx = chartCanvas.getContext('2d');
		var chart = new chartjs(ctx, {
				type: data.chartType,
				data: {
						labels: data.chartLabels,
						datasets: [{
								label: 'Revenue',
								backgroundColor: 'rgb(255, 99, 132)',
								borderColor: 'rgb(255, 99, 132)',
								data: data.chartValues,
						}]
				}
		});

	});

</script>

<canvas bind:this={chartCanvas} id="myChart"></canvas>

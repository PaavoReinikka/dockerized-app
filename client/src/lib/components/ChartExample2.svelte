<script>
	import chartjs from 'chart.js/auto';
	import { onMount } from 'svelte';

    let { chartData } = $props();
    let ctx;
	let chartCanvas;

    // onMount is a lifecycle function that runs when the component is mounted
    // it is similar to componentDidMount in React
	onMount(async (promise) => {
        // get the data from the API
		ctx = chartCanvas.getContext('2d');
		var chart = new chartjs(ctx, {
				type: chartData.chartType,
				data: {
						labels: chartData.chartLabels,
						datasets: [{
								label: 'Revenue',
								backgroundColor: 'rgb(255, 99, 132)',
								borderColor: 'rgb(255, 99, 132)',
								data: chartData.chartValues,
						}]
				}
		});

	});

</script>

<canvas bind:this={chartCanvas} id="myChart"></canvas>

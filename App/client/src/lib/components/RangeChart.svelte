<script>
    import chartjs from 'chart.js/auto';
    import { onMount } from 'svelte';
    import { readPriceRange } from '$lib/apis/data-api';



    

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

    let ctx;
    let chartCanvas;

    

    // Get the price values for the chart
    const chartValues = filteredData.map(item => item.price);
   
   onMount(async () => {
    
    ctx = chartCanvas.getContext('2d');
    new chartjs(ctx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Sähkön hinta',
                backgroundColor: 'rgb(70, 50, 255)',
                borderColor: 'rgb(255, 255, 255)',
                data: chartValues,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    ticks: {
                        maxRotation: 60,
                        minRotation: 60
                    }
                }
            },

			plugins: {
        	tooltip: {
            callbacks: {
                title: function(context) {
                    const idx = context[0].dataIndex;
                    const item = filteredData[idx];
                    const date = new Date(item.startDate);
                    const day = String(date.getUTCDate()).padStart(2, '0');
                    const month = String(date.getUTCMonth() + 1).padStart(2, '0');
                    const year = date.getUTCFullYear();
                    const hour = String(date.getUTCHours()).padStart(2, '0');
                    const minute = String(date.getUTCMinutes()).padStart(2, '0');
                    return `${day}.${month}.${year} ${hour}:${minute}`;
                }
            }
        }
    }
        },

    });
});
</script>

<canvas bind:this={chartCanvas} id="rangeChart" class="
	bottom-10
	top-10
	m-auto
	rounded"
 style="width: 100%;background-color: #1e1e2f;"
></canvas>


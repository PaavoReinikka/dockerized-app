<script>
    import PriceBall from "$lib/components/layout/PriceBall.svelte";
    import MainChart from "$lib/components/MainChart.svelte";
    import { onMount } from "svelte";
    import { usePricesState } from "$lib/states/usePricesState.svelte";
    import { readPriceRange } from "$lib/apis/data-api.js";
    import ChartTypeMenu from "$lib/components/ChartTypeMenu.svelte";

    const { data: pricesState } = usePricesState();
    

    // Function to calculate the average price for the day
    const averageDayPrice = array => array.reduce((a, b) => a + b) / array.length;

    let currentPrice = null; // Default value for current price
    let prices = null; // Store the fetched prices
    let loading = true; // Loading state
    let error = null; // Error state
    let dailyAverage = null; // Store the calculated daily average
    let weekAvgPrice = null; // Store the calculated weekly average
    let currentHourLabel = '';
    let matchingPrice = null; // Store the matching price for the current hour


    //let chartType = $state("bar"); // Default chart type

    let today = new Date();
    today.setUTCHours(0, 0, 0, 0); // Set to midnight UTC

    const weekAgo = new Date(today);
    weekAgo.setUTCDate(weekAgo.getUTCDate() - 7);

    async function fetchWeekAvgPrice() {
        try {
            const response = await readPriceRange(weekAgo.toISOString(), today.toISOString());
            const prices = response.map(p => p.price);
			const avg = averageDayPrice(prices);
			weekAvgPrice = avg.toFixed(3);
			console.log("Weekly Average:", weekAvgPrice);
        } catch (error) {
            console.error('Error fetching weekly prices:', error);
        }
}

    // Calculate the current price and daily average
    onMount(async () => {
        const prices = usePricesState();
        await prices.load();
        const pricesState = prices.data; 

        if (pricesState) {
            console.log("Chart Values:", pricesState);
            const now = new Date();
            const currentHour = now.getUTCHours();
            const currentDate = now.toISOString().split("T")[0];

            // Find the current price
            matchingPrice = pricesState.find(price => {
                const priceDate = new Date(price.startDate);
                return (
                    priceDate.getUTCHours() === currentHour &&
                    priceDate.toISOString().startsWith(currentDate)
                );
            });

            if (matchingPrice) {
                currentHourLabel = new Date(matchingPrice.startDate).toLocaleString('fi-FI', {
                    timeZone: 'Europe/Helsinki',
                    hour: '2-digit',
                    minute: '2-digit'
            });
        }


            currentPrice = matchingPrice ? matchingPrice.price : "N/A";

            // Calculate the daily average
            dailyAverage = averageDayPrice(pricesState.map(p => p.price)).toFixed(3);

            await fetchWeekAvgPrice();
        }
    });


    //let { data, form } = $props();
</script>

<h1 id="mainheading" class="text-center">
    <span class="text-xl">Market Electricity Prices<br> {new Date().toLocaleDateString()}</span>
    <br>
</h1>
<main class="flex gap-10 max-w-4xl mx-auto">
    <div class="text-center gap-5 flex flex-col mb-10">
       <PriceBall heading={`Sähkönhinta NYT (${currentHourLabel})`} price={currentPrice} timestamp={matchingPrice?.startDate}/>
       <PriceBall heading="Sähkö 24h" price={dailyAverage}/>
       <PriceBall heading="Sähkö viikko" price={weekAvgPrice}/>  
    </div>
    
    <MainChart />
</main>
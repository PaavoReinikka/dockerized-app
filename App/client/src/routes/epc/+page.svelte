<script>
    import PriceCards from '$lib/components/PriceCards.svelte';
    import chartjs from 'chart.js/auto';
    import { getTomorrow } from '$lib/utils/date-helpers.js';
    import { enhance } from '$app/forms';
    import { onMount } from 'svelte';

    let { form } = $props();
    let startTime = $state(form?.startTime || "");
    let endTime = $state(form?.endTime || "");
    let selection = $state(form?.selection || "both");
    const maxDate = getTomorrow();

    let labels = form?.labels || [];
    let productionValues = form?.productionValues || [];
    let consumptionValues = form?.consumptionValues || [];
    let differenceValues = form?.differenceValues || [];
    let priceLabels = form?.priceLabels || [];
    let prices = form?.priceValues || [];

    let chartCanvas;
    let chart;
    let chartType = $state("bar");

    let isLoading = $state(false);
    let selectedValues1 = $state([]);
    let selectedValues2 = $state([]);
    let kind1 = $state("");
    let kind2 = $state("");
    let units1 = $state("");
    let units2 = $state("");

    let dataLoader = $state(false);

    const getChartData = () => {
        if (selection === "both") {
            return {
                labels,
                datasets: [
                    {
                        label: 'Production',
                        backgroundColor: 'rgba(245, 39, 157, 0.5)',
                        borderColor: 'rgb(245, 39, 157)',
                        data: productionValues,
                        yAxisID: 'y',
                    },
                    {
                        label: 'Consumption',
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgb(54, 162, 235)',
                        data: consumptionValues,
                        yAxisID: 'y',
                    }
                ]
            };
        } else if (selection === "difference") {
            return {
                labels,
                datasets: [
                    {
                        label: 'Production - Consumption',
                        backgroundColor: 'rgba(157,39, 245, 0.7)',
                        borderColor: 'rgb(157,39, 245)',
                        data: differenceValues,
                        yAxisID: 'y',
                    }
                ]
            };
        } else if (selection === "price") {
            return {
                labels: priceLabels,
                datasets: [
                    {
                        label: 'Price',
                        backgroundColor: 'rgba(75, 192, 192, 0.7)',
                        borderColor: 'rgb(75, 192, 192)',
                        data: prices,
                        yAxisID: 'y',
                    }
                ]
            };
        }
        return { labels: [], datasets: [] };
    };

    const toggleChartType = () => {
        chartType = chartType === "line" ? "bar" : "line";
        if (chart) {
            chart.config.type = chartType;
            chart.update();
        }
    };

    onMount(() => {
        chart = new chartjs(chartCanvas.getContext('2d'), {
            type: chartType,
            data: getChartData(),
            options: {
                responsive: true,
                interaction: { mode: 'index', intersect: false },
                stacked: false,
                plugins: { title: { display: false } },
                scales: { y: { type: 'linear', display: true, position: 'left' } }
            }
        });
    });

    $effect(() => {
        // Update local state from form after submit
        if (form) {
            labels = form.labels || [];
            productionValues = form.productionValues || [];
            consumptionValues = form.consumptionValues || [];
            differenceValues = form.differenceValues || [];
            priceLabels = form.priceLabels || [];
            prices = form.priceValues || [];
            startTime = form.startTime || "";
            endTime = form.endTime || "";
        }
        // Update chart data
        if (chart) {
            const data = getChartData();
            chart.data.labels = data.labels;
            chart.data.datasets = data.datasets;
            chart.update();
        }
        // Update cards
        if (selection === "both") {
            selectedValues1 = productionValues;
            selectedValues2 = consumptionValues;
            kind1 = "prod.";
            kind2 = "cons.";
            units1 = "MWh";
            units2 = "MWh";
        } else if (selection === "difference") {
            selectedValues1 = differenceValues;
            selectedValues2 = [];
            kind1 = "difference";
            kind2 = "";
            units1 = "MWh";
            units2 = "";
        } else if (selection === "price") {
            selectedValues1 = prices;
            selectedValues2 = [];
            kind1 = "price";
            kind2 = "";
            units1 = "c/kWh";
            units2 = "";
        }
        dataLoader = (labels.length > 0 || priceLabels.length > 0)
    });
</script>

<div class="max-w-4xl mx-auto" >
    <div style="margin-top: 4rem; width: 100%; max-width: 1200px;">
        <h1 class="text-center text-3xl py-8 mt-8 mb-4 font-extrabold text-gray-900 dark:text-white">
            Production vs. Consumption
        </h1>
        <div class="shadow-lg p-4 mb-4 border-1 border-primary-100 rounded-xl bg-white dark:bg-gray-800 transition-all duration-300">
            <canvas bind:this={chartCanvas} id="epcChart" class=""></canvas>
        </div>
        <br/>
        <form method="POST" use:enhance={() => {
                                    isLoading = true;
                                    return async ({update}) => {
                                        await update();
                                        isLoading = false;
                                    }
                                }}
            action="?/getCombinedRange" class="mx-auto w-full max-w-md space-y-4">
            <div class="flex items-center justify-between gap-1">
                <label class="label">
                    <span class="label-text">Start date</span>
                    <input  class="input preset-outlined-primary-500"
                            name="startTime"
                            id="startTime"
                            type="date"
                            required
                            bind:value={startTime}
                            max={maxDate}
                    />
                </label>
                <label class="label">
                    <span class="label-text">End date</span>
                    <input  class="input preset-outlined-primary-500"
                            name="endTime"
                            id="endTime"
                            type="date"
                            required
                            bind:value={endTime}
                            max={maxDate}
                    />
                </label>
                <label class="label">
                    <span class="label-text">Filter</span>
                    <select class="select preset-outlined-primary-500"
                            id="selection"
                            name="selection"
                            bind:value={selection}
                            disabled={!dataLoader}>
                        <option value="both">Prod./Cons.</option>
                        <option value="difference">Difference</option>
                        <option value="price">Price</option>
                    </select>
                </label>
            </div>
            <div class="flex items-center justify-between gap-1">
                <button class="w-full btn preset-filled-primary-500 hover:preset-filled-primary-500"
                        type="submit"
                        disabled={isLoading}>
                    {#if isLoading}
                        Loading...
                    {:else}
                        Retrieve data
                    {/if}
                </button>
                <button class="btn preset-outlined-primary-500 hover:preset-filled-primary-500"
                        type="button"
                        onclick={toggleChartType}
                        disabled={!dataLoader}>
                    Toggle Chart Type
                </button>
            </div>
        </form>
        <div class="mt-10">
            {#if form?.error}
                <div class="mt-10 text-center">
                    {form.error}
                </div>
            {/if}
            <div>
                <PriceCards values={selectedValues1} kind={kind1} unit={units1}/>
            </div>
            <div>
                <PriceCards values={selectedValues2} kind={kind2} unit={units2}/>
            </div>
        </div>
    </div>
</div>


<script>
    import PriceCards from '$lib/components/PriceCards.svelte';
    import chartjs from 'chart.js/auto';
    import { getTomorrow } from '$lib/utils/date-helpers.js';
    import { enhance } from '$app/forms';
    import { onMount } from 'svelte';

    let selection = $state("none");
    let { form } = $props();
    let startTime = $state(form?.startTime || "");
    let endTime = $state(form?.endTime || "");
    const maxDate = getTomorrow();

    // All datasets
    let plainPriceLabels = form?.plainPriceLabels || [];
    let plainPriceValues = form?.plainPriceValues || [];
    let weekdayPriceLabels = form?.weekdayPriceLabels || [];
    let weekdayPriceValues = form?.weekdayPriceValues || [];
    let hourlyPriceLabels = form?.hourlyPriceLabels || [];
    let hourlyPriceValues = form?.hourlyPriceValues || [];
    let selectedValues = $state([]);
    
    let priceCanvas;
    let priceChart;
    let chartType = $state("bar");
    let isLoading = $state(false);

    let dataLoader = $state(false);
    //TODO: Weekday avg. not active if less than week of data

    const toggleChartType = () => {
        chartType = chartType === "line" ? "bar" : "line";
        priceChart.config.type = chartType;
        priceChart.update();
    };

    const getSelectedLabels = () => {
        if (selection === "weekdays") return weekdayPriceLabels;
        if (selection === "hourly") return hourlyPriceLabels;
        return plainPriceLabels;
    }
    const getSelectedValues = () => {
        if (selection === "weekdays") return weekdayPriceValues;
        if (selection === "hourly") return hourlyPriceValues;
        return plainPriceValues;
    }

    // Chart initialization
    onMount(() => {
        priceChart = new chartjs(priceCanvas.getContext('2d'), {
            type: chartType,
            data: {
                labels: getSelectedLabels(),
                datasets: [{
                    label: 'Price',
                    backgroundColor: 'rgba(10, 200, 245, 0.7)',
                    borderColor: 'rgb(10, 200, 245)',
                    data: getSelectedValues()
                }]
            },
            options: {
                responsive: true,
                interaction: { mode: 'index', intersect: false },
                plugins: { title: { display: false } },
            }
        });
    });

    $effect(() => {
        // Update local state from form after submit
        if (form) {
            plainPriceLabels = form.plainPriceLabels || [];
            plainPriceValues = form.plainPriceValues || [];
            weekdayPriceLabels = form.weekdayPriceLabels || [];
            weekdayPriceValues = form.weekdayPriceValues || [];
            hourlyPriceLabels = form.hourlyPriceLabels || [];
            hourlyPriceValues = form.hourlyPriceValues || [];
            startTime = form.startTime || "";
            endTime = form.endTime || "";
        }
        // Always update chart if chart exists (hacky way to ensure reactivity)
        if (priceChart) {
            priceChart.data.labels = getSelectedLabels();
            priceChart.data.datasets[0].data = getSelectedValues();
            priceChart.update();
        }
        if (selection === "none") {
            selectedValues = plainPriceValues;
        } else if (selection === "weekdays") {
            selectedValues = weekdayPriceValues;
        } else if (selection === "hourly") {
            selectedValues = hourlyPriceValues;
        }
        dataLoader = (plainPriceLabels.length > 0 ||
                      weekdayPriceLabels.length > 0 ||
                      hourlyPriceLabels.length > 0);
    });

</script>

<div class="max-w-4xl mx-auto" >
    <div style="margin-top: 4rem; width: 100%; max-width: 1200px;">
        <h1 id="" class="text-center text-3xl py-8 mt-8 mb-4 font-extrabold text-gray-900 dark:text-white">
            Electricity Market Price
        </h1>
        <div class="shadow-lg p-4 mb-4 border-1 border-primary-100 rounded-xl bg-white dark:bg-gray-800 transition-all duration-300">
            <canvas bind:this={priceCanvas}
                    id="priceChart"
                    class=""
                    ></canvas>
        </div>
        <br />
        <div class="">
            <form method="POST" use:enhance={() => {
                                        isLoading = true;
                                        return async ({update}) => {
                                            await update();
                                            isLoading = false;
                                        }
                                    }}
                action="?/getPriceRangeAll" class="mx-auto w-full max-w-md space-y-4">
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
                        <span class="label-text">Averaging</span>
                        <select class="select preset-outlined-primary-500"
                                bind:value={selection}
                                id="selection"
                                disabled={!dataLoader}>
                            <option value="none">None</option>
                            <option value="weekdays">Weekdays avg</option>
                            <option value="hourly">Hourly avg.</option>
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
        </div>
            {#if form?.error}
                <div class="mt-10 text-center">
                    {form.error}
                </div>
            {/if}
            <div class="py-8">
                <PriceCards values={selectedValues} kind="price" unit="c/kWh"/>
            </div>
    </div>
</div>



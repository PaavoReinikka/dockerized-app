<script>
    import ChartExample1 from "$lib/components/ChartExample1.svelte";
    import ChartExample2 from "$lib/components/ChartExample2.svelte";
    // WE CAN GET THE USER INFO THIS WAY
    let { data, form } = $props();
    let showChart = $state(false);
    const toggleChart = () => {
        showChart=!showChart;
    };
</script>

<!-- IF YOU WANT TO SEE THE DATA OBJECT, UNCOMMENT THIS
<p>{JSON.stringify(data)}</p>
-->

<nav>
<h1 id="minorheading" class="text-2xl text-center">
    This is a profile page
</h1>
<p class="text-center">
    We can add user information here, like name, email, etc.
    <br/>using Svelte stores to manage state. As an example,
    <br/>see the left upper corner for the user's email.
</p>
</nav>


<nav>
    <h1 id="minorheading" class="text-2xl text-center">
        Chart Example 1 (server side call)
    </h1>
</nav>

<!--Form with only a submit button to retirieve data using form action
retrieveData-->
<form method="post" action="?/retrieveData">
    <button type="submit" class="btn btn-primary bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Retrieve Private Data</button>
</form>

{#if form?.success}
    <ChartExample2 chartData={form.chartData} />
{/if}

{#if form?.error}
    <p class="text-xl text-red-500">{form.error}</p>
{/if}


<nav>
    <h1 id="minorheading" class="text-2xl text-center">
        Chart Example 2 (client side call)
    </h1>
</nav>

<button class="btn btn-primary bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
 onclick={toggleChart}>
    {showChart ? "Hide Chart" : "Show Chart"}
</button>
{#if showChart}
    <ChartExample1 />
{/if}
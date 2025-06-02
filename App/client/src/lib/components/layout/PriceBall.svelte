<script lang="ts">
    let { heading, price, timestamp } = $props();  
</script>

<div id="priceBall" class="flex flex-col justify-center items-center rounded-full bg-blue-500 w-50 h-50">
    <p class="font-bold">{heading}</p>
    <span>{price}(snt / kWh)</span>

    {#if timestamp}
		<p class="text-xs text-gray-200 mt-1">
			Päivitetty: {new Date(timestamp).toLocaleString('fi-FI', {
				timeZone: 'Europe/Helsinki',
				hour: '2-digit',
				minute: '2-digit',
				day: '2-digit',
				month: '2-digit'
			})} EEST
		</p>
	{/if}
</div>
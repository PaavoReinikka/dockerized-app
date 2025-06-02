<script>
    let { chartType = $bindable() } = $props();
</script>
<div class="mb-4 w-full max-w-xs">
	<label for="taulukko" class="block mb-1 text-sm text-white">Valitse kaaviotyyppi</label>
	<select
		id="taulukko"
		bind:value={chartType}
		class="w-full px-3 py-2 rounded bg-gray-800 text-white border border-gray-600 text-sm"
	>
		<option value="bar">Pylväs</option>
		<option value="line">Viiva</option>
		<option value="radar">Tutka</option>
	</select>
</div>
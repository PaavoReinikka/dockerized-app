<script>
    import { getStats } from "$lib/utils/stats-helpers.js";
    let { values, kind, unit } = $props();
    let stats = $state({});
    $effect(() => {
        if (values && values.length > 0) {
            stats = getStats(values);
        } else {
            stats = undefined;
        }
    });
</script>

{#if stats}
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-label">Max {kind}</div>
            <div class="stat-value">{stats.max} {unit}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Min {kind}</div>
            <div class="stat-value">{stats.min} {unit}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Average {kind}</div>
            <div class="stat-value">{stats.mean} {unit}</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Std. {kind}</div>
            <div class="stat-value">{stats.std} {unit}</div>
        </div>
    </div>
{/if}


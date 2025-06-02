<script>
    import { clockStore } from "$lib/utils/clock.js";
    const clock = clockStore({interval: 1000})
</script>

<p class="font-bold px-4 text-left w-full">
    <span>{$clock}</span>
</p>

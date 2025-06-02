<script>
    let data = $props();
    let theme = "cerberus"; // default theme

    function setTheme(newTheme) {
        theme = newTheme;
        document.body.setAttribute("data-theme", newTheme);
    }
</script>


<!-- <footer class="p-4 bg-black border-t-1">
    <p class="text-center text-white font-bold">
        Dogs seem to dislike cats, sadly... © 2025
    </p>
</footer> -->
<footer class="p-4 bg-black border-t-1">
    <div class="flex items-center justify-between">
        <button class="btn btn-sm text-white" onclick={() => setTheme("cerberus")}>Cerberus</button>
        <button class="btn btn-sm text-white" onclick={() => setTheme("crimson")}>Crimson</button>
        <button class="btn btn-sm text-white" onclick={() => setTheme("legacy")}>Legacy</button>
        <button class="btn btn-sm text-white" onclick={() => setTheme("nosh")}>Nosh</button>
        <button class="btn btn-sm text-white" onclick={() => setTheme("terminus")}>Terminus</button>
        <button class="btn btn-sm text-white" onclick={() => setTheme("catppuccin")}>Catppuccin</button>
        <button class="btn btn-sm text-white" onclick={() => setTheme("rocket")}>Rocket</button>
    </div>
    <!-- <p class="text-center text-white font-bold flex-1">
        Dogs seem to dislike cats, sadly... © 2025
    </p> -->
</footer>

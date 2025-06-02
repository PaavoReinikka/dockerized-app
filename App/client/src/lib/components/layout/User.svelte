<script>
    let { user } = $props();
</script>

{#if user?.email}
    <p class="text-right text-gray-900 dark:text-white w-full px-4">
        Logged in as: <b>{user.email}</b>
    </p>
{/if}

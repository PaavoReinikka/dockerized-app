<script>
    let { user } = $props();
</script>

{#if user?.email}
    <p class="text-right text-gray-900 dark:text-white w-full px-4" id="user-info">
        Logged in as: <b>{user.email}</b>
    </p>
{/if}

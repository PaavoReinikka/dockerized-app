<script>
    let { data, form } = $props();
</script>

<div class="max-w-xl mx-auto mt-20">
<h1 id="minorheading" class="text-center"><!--class="text-xl pb-4"> h2-->
    Confirm your logout
</h1>

{#if form?.error}
    <div class="alert alert-error">
        {form.error}
    </div>
{/if}

{#if form?.message}
    <div class="alert alert-success">
        {form.message}
    </div>
{/if}

{#if data?.removed}
    <p class="text-xl text-center">
        Your account has been removed.
    </p>
{/if}

{#if data?.remove_error}
    <p class="text-xl">
        User account could not be removed.<br/>contact site admin: eprice.varmennus@gmail.com.
    </p>
{/if}


    <form method="POST" action="?/logout" class="p-8">
        <button class="w-full btn preset-filled-primary-500" type="submit">Logout</button>
    </form>
</div>

<script>
    let { data, form } = $props();
</script>

<h1 id="minorheading" class="text-center">
    Resend Verification Email
</h1>
  
{#if form?.message}
<p class="text-xl">{form.message}</p>
{/if}

{#if form?.error}
<p class="text-xl text-red-500">{form.error}</p>
{/if}

<form class="space-y-4" method="POST" action="?/resend" enctype="application/json">
    <label class="label" for="email">
        <span class="label-text">Email</span>
        <input
            class="input"
            id="email"
            name="email"
            type="email"
            placeholder="Email"
            required />
    </label>
    <button class="w-full btn preset-filled-primary-500" type="submit">
      Send
    </button>
</form>

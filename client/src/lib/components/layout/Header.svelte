<script>
  import bg from "$lib/assets/image.png";
  let { user } = $props();
</script>

<header class="flex items-center bg-primary-100 p-4 mb-6" style="background-image: url({bg})">
<!--<header class="flex items-center bg-primary-300 p-4 mb-6">-->
  <h1 class="text-2xl text-white items-center">Electricity prices</h1>
    <nav>
      <ul class="ml-4 flex space-x-4 underline text-white">
        <li>
          <a href="/" class="">Home</a>
        </li>
        {#if user}
      <ul class="ml-4 flex space-x-4 underline text-white">
        <li>
          <a href="/profile" class="">Profile</a>
        </li>
      </ul>
        {:else}
            <li>
              <a href="/auth/login" class="">Login</a>
            </li>
            <li>
              <a href="/auth/register" class="">Register</a>
            </li>
        {/if}
      </ul>
    </nav>
    {#if user}
      <div class="ml-auto">
        <a href="/logout"  data-sveltekit-reload data-sveltekit-preload-data="false" 
        class="btn bg-primary-300 hover:bg-primary-500 text-white">Logout</a>
      </div>
    {/if}
</header>
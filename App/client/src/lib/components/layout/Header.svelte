<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  let { user } = $props();

  let devChatAvailable = $state(false);

  onMount(async () => {
    const res = await fetch('/api/devchat');
    const data = await res.json();
    devChatAvailable = data.available;
  });
</script>

<header class="flex items-center justify-between bg-black drop-shadow-xl backdrop-blur-lg p-4 mb-2">
<!--<header class="flex items-center bg-primary-300 p-4 mb-6">-->
  <h1 class="text-2xl text-white">Electricity prices</h1>
    <nav>
      <ul class="ml-4 flex space-x-4 text-white">
        <li>
          <a href="/" class="">Home</a>
        </li>
        {#if user}
        <li>
          <a href="/epc" id="epc-link" class="">Production/Consumption</a>
        </li>
        <li>
          <a href="/price" id="price-link" class="">Price</a>
        </li>
        {:else}
            <li>
              <a href="/auth/login" id="login-link" class="">Login</a>
            </li>
            <li>
              <a href="/auth/register" id="register-link" class="">Register</a>
          </li>
        {/if}
      </ul>
    </nav>
    {#if user && $page.url.pathname !== '/logout'}
      <div class="ml-auto">
        <ul class="ml-4 flex space-x-4 text-white">
          {#if user.role === 'admin' && devChatAvailable}
            <li>
              <a href="/chat" id="developer-chat-link" class="underline text-white font-bold">Developer Chat</a>
            </li>
          {/if}
          <li>
            <a href="/auth/remove" id="delete-link" class="underline text-white">Delete account</a>
          </li>
          <li>
            <a href="/logout" class="underline text-white" id="logout-link">Logout</a>
          </li>
        </ul>
      </div>
    {:else if $page.url.pathname === '/logout'}
      <div class="ml-auto">
        <!--This is a hack to force the placement of other elements-->
      </div>
    {/if}
</header>
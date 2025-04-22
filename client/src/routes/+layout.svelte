<script>
    import "../app.css";
    import { useUserState } from "$lib/states/userState.svelte.js";
    import Header from "$lib/components/layout/Header.svelte";
    import Footer from "$lib/components/layout/Footer.svelte";
    import ChatBot from "$lib/components/ChatBot.svelte";

    
    let { children, data } = $props();
    const userState = useUserState();
    if (data.user) {
      userState.user = data.user;
    }

  </script>

<div class="flex flex-col h-full">
  
  
  <Header user={data.user} />

  {#if data.user?.email}
    <p class="">
      Logged in as:<br/> <b>{data.user?.email}</b>
    </p>

    <ChatBot user={data.user} />
  {/if}
  
  <main class="container mx-auto max-w-2xl grow">
    {@render children()}
  </main>

  <Footer />
  
</div>
<script>
    import "../app.css";
    import { useUserState } from "$lib/states/userState.svelte.js";
    import Header from "$lib/components/layout/Header.svelte";
    import Footer from "$lib/components/layout/Footer.svelte";
    import Clock from "$lib/components/layout/Clock.svelte";
    import User from "$lib/components/layout/User.svelte";
    import ChatBot from "$lib/components/ChatBot.svelte";

    
    let { children, data } = $props();
    const userState = useUserState();
    if (data.user) {
      userState.user = data.user; // for future use in components
    }

  </script>

<div class="flex flex-col h-full">
  
  
  <Header user={data.user} />
  <div class="flex row">
    <Clock />
    <User user={data.user} />
  </div>
  
  <main class="container grow mx-auto">
    {@render children()}
  </main>

  {#if data.user?.role === "admin"}
    <ChatBot user={data.user} />
  {/if}

  <Footer />
  
</div>

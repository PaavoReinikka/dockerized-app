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
      userState.user = data.user;
    }

  </script>

<div class="flex flex-col h-full">
  
  
  <Header user={data.user} />
  <div class="flex row">
    <Clock />
    <User user={data.user} />
  </div>

  {#if data.user?.email}
    <!-- <p class="text-right text-gray-500 dark:text-gray-400">
      Logged in as: <b>{data.user?.email}</b>
    </p> -->

    <ChatBot user={data.user} />
  {/if}
  
  <main class="container grow mx-auto"> <!-- mx-auto grow max-w-4xl-->
    {@render children()}
  </main>

  <Footer />
  
</div>

<!--
<style>
  :global(body){
  background-image: url("https://images.pexels.com/photos/956981/milky-way-starry-sky-night-sky-star-956981.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-position: center;
  font-family: 'Poppins', sans-serif;
  font-size: 1.2rem
  }
</style>
-->
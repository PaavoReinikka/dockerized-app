<script>
    let { data, form } = $props();
    let title = $state("");
    let email = $state("");
    let code = $state("");

    $effect(() => {
        if (data.action === "login") {
            title = "Login";
        } else if (data.action === "register") {
            title = "Register";
        } else if (data.action === "verify") {
            title = "Verify";
        } else if (data.action === "remove") {
            title = "Remove";
        }
        if (data.code && data.action === "verify") {
            code = data.code;
        }
        if (data.email) {
            email = data.email;
        }
    });

</script>

<div class="max-w-xl mx-auto mt-20" >
  <h1 id="minorheading" class="text-center"><!--class="text-xl pb-4"> h2-->
    {title} Form<!--{data.action === "login" ? "Login" : "Register"} form-->
  </h1>
  
  {#if form?.message}
    <p class="text-xl">{form.message}</p>
  {/if}

  <!-- {#if form?.error}
    <p class="text-xl text-red-500">{form.error}</p>
  {/if} -->

  {#if data.registered}
    <p class="text-xl">
      Verification has been sent to your email. Please verify your account to continue.
    </p><br/>
  {/if}

  {#if data.is_verified}
    <p class="text-xl">
      Your email has been verified. You can now login.
    </p><br/>
  {/if}

  {#if form?.message==="Email not verified."}
    <p class="text-xl">
      Please check your email for the verification code.
    </p><br/>
  {/if}



  <form class="space-y-4" method="POST" action="?/{data.action}" enctype="application/json">
    <label class="label" for="email">
      <span class="label-text">Email</span>
      <input
        class="input"
        id="email"
        name="email"
        type="email"
        placeholder="Email"
        bind:value={email}
        required
      />
    </label>
    {#if data.action === "verify"}
      <label class="label" for="code">
        <span class="label-text">Verification Code</span>
        <input
          class="input"
          id="code"
          name="code"
          type="text"
          bind:value={code}
          required
        />
      </label>
    <!--else if login or register, show password-->
    {:else}
      <label class="label" for="password">
        <span class="label-text">Password</span>
        <input 
          class="input"
          id="password"
          name="password"
          type="password"
          required />
      </label>
    {/if}
    <button class="w-full btn preset-filled-primary-500" type="submit">
      {title}<!-- === "login" ? "Login" : "Register"}-->
    </button>
  </form>


  {#if form?.message==="Email not verified."}
  <br/>
  <div class="flex gap-2">
    <a href="/send" class="btn preset-filled-primary-500">
      Resend Verification Email
    </a>
    <a href="/auth/verify" class="btn preset-filled-primary-500 w-full">
      Verify Email
    </a>
  </div>
  <br/>
{/if}
</div>
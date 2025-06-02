<script>
    // import { PUBLIC_CHAT_URL2 } from "$env/static/public";
    import { PUBLIC_USER_CHAT_URL } from "$env/static/public";
    
    let chatOnState = $state(false);
    const toggleChat = () => {
        chatOnState = !chatOnState;
    };
    let user = $props();

</script>

<!-- Styles like chat-toggle are in app.css (mix with tailwind) -->
<button
    class="text-primary-500 font-bold  px-4 rounded chat-toggle {chatOnState ? '' : 'hidden'}"
    onclick={toggleChat}>
    {chatOnState ? 'Hide Chat' : 'Open Chat'}
</button>

{#if chatOnState}
    <div class="rounded-lg shadow-lg">
        <div class="gradio-embed" style="position: fixed; bottom: 0; right: 0; width: 400px; height: 800px; z-index: 9999;">
            <iframe title="Gradio App"
                src="{PUBLIC_USER_CHAT_URL}"
                width="100%"
                height="100%"
                frameborder="20"
                allowfullscreen
                name="gradio-iframe"
                class="rounded-t-lg"
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
            ></iframe>
        </div>
    </div>
{/if}

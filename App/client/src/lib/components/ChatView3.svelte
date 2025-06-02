<script>
    import { PUBLIC_CHAT_URL1 } from "$env/static/public";
</script>

<style>
    .gradio-embed {
        width: 100%;
        height: 70vh; /* Adjust as needed, or use 100% if your layout is flex */
        margin: 0;
        padding: 0;
    }
    .gradio-embed iframe {
        width: 100%;
        height: 100%;
        border: none;
        display: block;
    }
</style>

<div class="gradio-embed" data-gradio-embed="false">
    <iframe title="Gradio App"
        src={PUBLIC_CHAT_URL1}
        allowfullscreen
        name="gradio-iframe"
        sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
    ></iframe>
</div>
<script>
    import ChatView1 from "$lib/components/ChatView1.svelte";
    import ChatView2 from "$lib/components/ChatView2.svelte";
    import ChatView3 from "$lib/components/ChatView3.svelte";
    import ChatView4 from "$lib/components/ChatView4.svelte";
    import Tabs from "$lib/components/Tabs.svelte";

    let activeTabValue = $state(4);

    let items = [
        { label: "Streaming",
            value: 1,
            component: ChatView1
            },
        { label: "Agent",
            value: 2,
            component: ChatView2
            },
        { label: "Files",
            value: 3,
            component: ChatView3
        },
        { label: "Docs",
            value: 4,
            component: ChatView4
        }
    ];
</script>


<Tabs items={items} activeTabValue={activeTabValue} on:change={e => activeTabValue = e.detail} />
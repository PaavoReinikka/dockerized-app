<script>
  import { createEventDispatcher } from 'svelte';
  
  let { activeTabValue, items } = $props();

  const dispatch = createEventDispatcher();

  const handleClick = tabValue => () => dispatch('change', tabValue);
  let size=$state("");

  $effect(() => {
    //This is really hacky, but it works for now
    const activeItem = items.find(item => item.value === activeTabValue);
    if (activeItem && activeItem.label === "Agent") {
      size = "max-auto";
    } else {
      size = "max-w-3xl";
    }
  });
</script>

<div class="mx-auto {size} mt-12">
    <ul>
    {#each items as item}
        <li class={activeTabValue === item.value ? 'active' : ''}>
            <button type="button" onclick={handleClick(item.value)}
                    class="tab-btn"
            >{item.label}
            </button>
        </li>
    {/each}
    </ul>
    {#each items as item}
        {#if activeTabValue == item.value}
        <div class="box">
            <item.component />
        </div>
        {/if}
    {/each}
</div>


<style>
	.box {
		margin-bottom: 0px;
		padding: 0px;
		/* border: 1px solid #dee2e6; */
    border-radius: 0.5rem; /* Rounded all corners */
    border: 0px solid var(--color-border, rgb(8, 40, 73)); /* Use preset or fallback */
    border-top: 0;
    /*background-image: url('$lib/assets/image3.png'); /* <-- Add this line */
    background-size: cover;               /* Optional: cover the box */
    background-repeat: no-repeat;         /* Optional: no repeat */
    background-position: center;
	}
  ul {
    display: flex;
    flex-wrap: wrap;
    padding-left: 0;
    margin-bottom: 0;
    list-style: none;
    border-bottom: 1px solid #dee2e6;
  }
	li {
		margin-bottom: -1px;
	}

  .tab-btn {
    border: 1px solid transparent;
    border-top-left-radius: 0.25rem;
    border-top-right-radius: 0.25rem;
    display: block;
    padding: 0.5rem 1rem;
    cursor: pointer;
    background: none;
    color: inherit;
    font: inherit;
    outline: none;
  }

  .tab-btn:hover {
    border-color: #e9ecef #e9ecef #dee2e6;
  }

  li.active > .tab-btn {
    color: #495057;
    background-color: #fff;
    border-color: #dee2e6 #dee2e6 #fff;
  }
</style>

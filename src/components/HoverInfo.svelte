<script>
  export let text = "";
  let hovered = false;
</script>

<div
  class="relative inline-block"
  on:mouseenter={() => hovered = true}
  on:mouseleave={() => hovered = false}
>
  <slot></slot>
  {#if hovered}
    <div class="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 bg-black text-white text-xs rounded py-1 px-2 whitespace-nowrap">
      {text}
    </div>
  {/if}
</div>

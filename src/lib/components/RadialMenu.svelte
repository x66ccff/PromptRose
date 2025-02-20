<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let items: Array<{
    id: string;
    label: string;
    icon?: string;
  }> = [];

  export let radius: number = 150;
  export let innerRadius: number = 50;
  export let isOpen: boolean = false;

  let menuElement: HTMLDivElement;
  let itemElements: HTMLDivElement[] = [];
  let centerX: number = 0;
  let centerY: number = 0;

  $: if (isOpen) {
    positionItems();
  }

  function positionItems() {
    const angleStep = (2 * Math.PI) / items.length;
    
    itemElements.forEach((element, index) => {
      if (!element) return;
      
      const angle = index * angleStep - Math.PI / 2; // Start from top
      const x = centerX + radius * Math.cos(angle);
      const y = centerY + radius * Math.sin(angle);
      
      element.style.transform = `translate(${x}px, ${y}px)`;
      element.style.opacity = '1';
    });
  }

  function handleMouseMove(event: MouseEvent) {
    if (!isOpen) return;
    
    const rect = menuElement.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    
    itemElements.forEach((element, index) => {
      if (!element) return;
      
      const itemRect = element.getBoundingClientRect();
      const itemX = itemRect.left + itemRect.width / 2 - rect.left;
      const itemY = itemRect.top + itemRect.height / 2 - rect.top;
      
      const distance = Math.sqrt(
        Math.pow(x - itemX, 2) + Math.pow(y - itemY, 2)
      );
      
      const scale = distance < 50 ? 1.2 : 1;
      element.style.transform += ` scale(${scale})`;
    });
  }

  onMount(() => {
    if (menuElement) {
      const rect = menuElement.getBoundingClientRect();
      centerX = rect.width / 2;
      centerY = rect.height / 2;
    }
  });
</script>

<div
  class="radial-menu"
  class:open={isOpen}
  bind:this={menuElement}
  on:mousemove={handleMouseMove}
>
  <div class="center-circle" style="width: {innerRadius * 2}px; height: {innerRadius * 2}px;">
    <slot name="center">
      <span class="center-icon">☰</span>
    </slot>
  </div>
  
  {#each items as item, i}
    <div
      class="menu-item"
      bind:this={itemElements[i]}
      data-id={item.id}
      on:click={() => dispatch('itemClick', item)}
    >
      {#if item.icon}
        <span class="icon">{item.icon}</span>
      {/if}
      <span class="label">{item.label}</span>
    </div>
  {/each}
</div>

<style>
  .radial-menu {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 400px;
    height: 400px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .radial-menu.open {
    opacity: 1;
    pointer-events: all;
  }

  .center-circle {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.8);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    cursor: pointer;
    z-index: 2;
  }

  .center-icon {
    font-size: 24px;
  }

  .menu-item {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 12px 20px;
    border-radius: 25px;
    display: flex;
    align-items: center;
    gap: 8px;
    opacity: 0;
    transition: all 0.3s ease;
    cursor: pointer;
    white-space: nowrap;
  }

  .menu-item:hover {
    background: rgba(0, 0, 0, 0.9);
  }

  .icon {
    font-size: 20px;
  }

  .label {
    font-size: 14px;
  }
</style>

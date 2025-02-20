<script lang="ts">
  import RadialMenu from './lib/components/RadialMenu.svelte';
  import { invoke } from '@tauri-apps/api/tauri';

  let isMenuOpen = false;
  let message = '';

  const menuItems = [
    { id: 'chat', label: '聊天', icon: '💬' },
    { id: 'image', label: '图像', icon: '🖼️' },
    { id: 'code', label: '代码', icon: '💻' },
    { id: 'audio', label: '音频', icon: '🎵' },
    { id: 'video', label: '视频', icon: '🎥' },
    { id: 'settings', label: '设置', icon: '⚙️' },
  ];

  function handleKeyDown(event: KeyboardEvent) {
    if (event.key === 'Alt') {
      isMenuOpen = true;
    }
  }

  function handleKeyUp(event: KeyboardEvent) {
    if (event.key === 'Alt') {
      isMenuOpen = false;
    }
  }

  async function handleMenuItemClick(item: { id: string; label: string }) {
    message = `已选择: ${item.label}`;
    
    switch (item.id) {
      case 'chat':
        message = '开始聊天...';
        break;
      case 'image':
        message = '处理图像...';
        break;
      case 'code':
        message = '编写代码...';
        break;
      case 'audio':
        message = '处理音频...';
        break;
      case 'video':
        message = '处理视频...';
        break;
      case 'settings':
        message = '打开设置...';
        break;
    }

    // 示例：调用后端函数
    try {
      // const response = await invoke('your_backend_function', { type: item.id });
      // message = `处理结果: ${response}`;
    } catch (error) {
      console.error('Error:', error);
      message = '操作失败，请重试';
    }
  }
</script>

<svelte:window on:keydown={handleKeyDown} on:keyup={handleKeyUp} />

<main>
  <div class="content">
    <h1>PromptRose 🌹</h1>
    <p class="instruction">按住 Alt 键打开菜单</p>
    {#if message}
      <p class="message">{message}</p>
    {/if}
  </div>

  <RadialMenu
    {items}
    bind:isOpen={isMenuOpen}
    radius={150}
    innerRadius={40}
    on:itemClick={e => handleMenuItemClick(e.detail)}
  />
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    margin: 0;
    font-family: system-ui, -apple-system, sans-serif;
  }

  .content {
    text-align: center;
    z-index: 1;
  }

  h1 {
    font-size: 2.5em;
    color: #2c3e50;
    margin-bottom: 0.5em;
  }

  .instruction {
    color: #7f8c8d;
    font-size: 1.2em;
    margin-bottom: 1em;
  }

  .message {
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 10px 20px;
    border-radius: 20px;
    font-size: 1.1em;
    margin-top: 2em;
    animation: fadeIn 0.3s ease;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>

<template>
  <div class="min-h-screen bg-background text-foreground font-sans">
    <header class="p-4 border-b border-border flex justify-between items-center">
      <h1 class="text-xl font-handwritten">Evsy</h1>
      <div>
        <slot name="actions" />
      </div>
    </header>

    <main class="p-4 md:p-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
// Theme toggle, user state и т.п. можно сюда добавить позже
</script>

<style scoped>
.font-handwritten {
  font-family: 'Pacifico', cursive;
}
</style>
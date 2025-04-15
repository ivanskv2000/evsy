<script setup lang="ts">
import { ref, provide } from 'vue'

const theme = ref<'light' | 'dark'>('light')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.classList.toggle('dark')
}

provide('theme', theme)
provide('toggleTheme', toggleTheme)
</script>

<template>
  <slot :theme="theme" :toggleTheme="toggleTheme" />
</template> 
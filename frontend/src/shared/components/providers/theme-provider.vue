<script setup lang="ts">
import { provide } from 'vue'
import { useColorMode } from '@vueuse/core'

const theme = useColorMode({
  attribute: 'class', // <- key part
  selector: 'html', // <- ensure it adds `class="dark"` to <html>
  emitAuto: false,
  storageKey: 'theme',
  disableTransition: false, // <- ensure transitions aren't skipped
})

const toggleTheme = () => {
  // disableTransitionsTemporarily()
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

provide('theme', theme)
provide('toggleTheme', toggleTheme)
</script>

<template>
  <slot :theme="theme" :toggleTheme="toggleTheme" />
</template>

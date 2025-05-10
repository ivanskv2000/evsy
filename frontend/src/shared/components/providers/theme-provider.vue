<script setup lang="ts">
import { provide } from 'vue'
import { useColorMode } from '@vueuse/core'

const theme = useColorMode({
  attribute: 'class',
  selector: 'html',
  emitAuto: false,
  storageKey: 'theme',
  disableTransition: false,
})

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
}

provide('theme', theme)
provide('toggleTheme', toggleTheme)
</script>

<template>
  <slot :theme="theme" :toggleTheme="toggleTheme" />
</template>

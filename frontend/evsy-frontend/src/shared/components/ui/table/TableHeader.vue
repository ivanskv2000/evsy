<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/shared/utils/general'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <thead data-slot="table-header" :class="cn('[&_tr]:border-b', props.class)">
    <slot />
  </thead>
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { useAttrs } from 'vue'
import { cn } from '@/shared/utils/general' // adjust path if needed

const props = defineProps<{
  icon: string
  label: string
  value?: string
}>()

const attrs = useAttrs()
</script>

<template>
  <div
    :class="cn('flex flex-wrap items-center gap-1', attrs.class as string | undefined)"
    v-bind="attrs"
  >
    <div class="mr-2 flex items-center gap-1">
      <Icon :icon="props.icon" class="h-4 w-4" />
      <span>{{ props.label }}:</span>
    </div>
    <span v-if="props.value">{{ props.value }}</span>
    <slot name="value" />
  </div>
</template>

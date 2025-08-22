<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { Input } from '@/shared/ui/input'
import { ref, watch, onMounted } from 'vue'
import { useDebounceFn } from '@vueuse/core'

interface DataTableInputFilterProps {
  column: Column<TData, TValue>
  placeholder: string
}

const props = defineProps<DataTableInputFilterProps>()

// Local state for the input value
const inputValue = ref<string>('')

// Debounced function to update the column filter
const debouncedUpdateFilter = useDebounceFn((value: string) => {
  props.column.setFilterValue(value || undefined)
}, 300)

// Watch for input changes and apply debounce
watch(inputValue, newValue => {
  debouncedUpdateFilter(newValue)
})

// Handle escape key to clear the filter
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    inputValue.value = ''
    props.column.setFilterValue(undefined)
  }
}

// Initialize with current filter value
onMounted(() => {
  const currentValue = props.column.getFilterValue() as string
  if (currentValue) {
    inputValue.value = currentValue
  }
})

// Watch for external filter changes (if filter is cleared programmatically)
watch(
  () => props.column.getFilterValue(),
  newValue => {
    const stringValue = (newValue as string) || ''
    if (stringValue !== inputValue.value) {
      inputValue.value = stringValue
    }
  }
)
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<template>
  <Input v-model="inputValue" :placeholder="placeholder" @keydown="handleKeydown" />
</template>

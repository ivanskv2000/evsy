<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { Input } from '@/shared/components/ui/input'

interface DataTableInputFilterProps {
  column: Column<TData, TValue>
  placeholder: string
}

defineProps<DataTableInputFilterProps>()
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<template>
  <Input
    :placeholder="placeholder"
    :model-value="column.getFilterValue() as string"
    @update:model-value="column.setFilterValue($event)"
  />
</template>

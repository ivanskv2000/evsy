<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/ui/select'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

interface DataTableInputFilterProps {
  column: Column<TData, TValue>
  placeholder: string
  options: string[]
  showClearButton: boolean
}

defineProps<DataTableInputFilterProps>()
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<template>
  <div class="flex items-center gap-1">
    <Select
      :model-value="column.getFilterValue() as string"
      @update:model-value="column.setFilterValue($event)"
    >
      <SelectTrigger>
        <SelectValue class="min-w-[12ch]" placeholder="Select a type..." />
      </SelectTrigger>
      <SelectContent>
        <SelectItem v-for="option in options" :key="option" :value="option">
          {{ option }}
        </SelectItem>
      </SelectContent>
    </Select>

    <Button :disabled="!showClearButton" variant="ghost" @click="column.setFilterValue('')">
      <Icon class="h-4 w-4" icon="radix-icons:cross-2" />
      <span class="sr-only">Clear type filter</span>
    </Button>
  </div>
</template>

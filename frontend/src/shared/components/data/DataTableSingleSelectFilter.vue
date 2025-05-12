<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/ui/select'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'
import { computed } from 'vue';

interface DataTableInputFilterProps {
  column?: Column<TData, TValue>
  title?: string
  placeholder: string
  options: string[]
  disabled?: boolean
}

const props = defineProps<DataTableInputFilterProps>()

const selectedValue = computed(() => props.column?.getFilterValue() as string)
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<template>
  <div class="flex items-center gap-1">
    <Select
      :model-value="selectedValue"
      @update:model-value="column?.setFilterValue($event)"
      :disabled="disabled"
    >
      <SelectTrigger>
        <SelectValue
          class="min-w-[12ch]"
          :placeholder="placeholder"
        >
          <template v-if="selectedValue">
            <span v-if="selectedValue">{{ selectedValue }}</span>
          </template>
        </SelectValue>
      </SelectTrigger>
      <SelectContent class="max-h-[400px]">
        <SelectItem v-for="option in options" :key="option" :value="option">
          {{ option }}
        </SelectItem>
      </SelectContent>
    </Select>

    <Button :disabled="!selectedValue" variant="ghost" @click="column?.setFilterValue('')">
      <Icon class="h-4 w-4" icon="radix-icons:cross-2" />
      <span class="sr-only">Clear type filter</span>
    </Button>
  </div>
</template>

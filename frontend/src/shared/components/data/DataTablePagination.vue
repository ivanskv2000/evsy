<script setup lang="ts" generic="TData">
import { type Table } from '@tanstack/vue-table'
import { Icon } from '@iconify/vue'
import { computed } from 'vue'
import { Button } from '@/shared/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/ui/select'

interface DataTablePaginationProps {
  table: Table<TData>
  pageSizeOptions?: number[]
}

const props = defineProps<DataTablePaginationProps>()

const defaultPageSizeOptions = [10, 20, 30, 40, 50]
const currentPageSize = computed(() => props.table.getState().pagination.pageSize)
const paginationOptions = computed(() => {
  const base = props.pageSizeOptions ?? defaultPageSizeOptions
  const set = new Set([...base, currentPageSize.value])
  return [...set].sort((a, b) => a - b)
})

const rowsSelected = computed(() => props.table.getFilteredSelectedRowModel().rows.length > 0)
</script>

<template>
  <div
    :class="{
      'flex items-center px-2': true,
      'justify-between': rowsSelected,
      'justify-end': !rowsSelected,
    }"
  >
    <div v-if="rowsSelected" class="text-muted-foreground flex-1 text-sm">
      {{ table.getFilteredSelectedRowModel().rows.length }} of
      {{ table.getFilteredRowModel().rows.length }} row(s) selected.
    </div>
    <div class="flex items-center space-x-4 lg:space-x-6">
      <div class="flex items-center space-x-2">
        <p class="text-sm font-medium">Rows per page</p>
        <Select
          :model-value="`${table.getState().pagination.pageSize}`"
          @update:model-value="value => table.setPageSize(Number(value))"
        >
          <SelectTrigger class="h-8 w-[70px]">
            <SelectValue :placeholder="`${table.getState().pagination.pageSize}`" />
          </SelectTrigger>
          <SelectContent side="top">
            <SelectItem
              v-for="pageSize in paginationOptions"
              :key="pageSize"
              :value="`${pageSize}`"
            >
              {{ pageSize }}
            </SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div class="flex w-[100px] items-center justify-center text-sm font-medium">
        Page {{ table.getState().pagination.pageIndex + 1 }} of
        {{ table.getPageCount() }}
      </div>
      <div class="flex items-center space-x-2">
        <Button
          variant="outline"
          class="hidden h-8 w-8 p-0 lg:flex"
          :disabled="!table.getCanPreviousPage()"
          @click="table.setPageIndex(0)"
        >
          <span class="sr-only">Go to first page</span>
          <Icon icon="radix-icons:double-arrow-left" class="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          class="h-8 w-8 p-0"
          :disabled="!table.getCanPreviousPage()"
          @click="table.previousPage()"
        >
          <span class="sr-only">Go to previous page</span>
          <Icon icon="radix-icons:chevron-left" class="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          class="h-8 w-8 p-0"
          :disabled="!table.getCanNextPage()"
          @click="table.nextPage()"
        >
          <span class="sr-only">Go to next page</span>
          <Icon icon="radix-icons:chevron-right" class="h-4 w-4" />
        </Button>
        <Button
          variant="outline"
          class="hidden h-8 w-8 p-0 lg:flex"
          :disabled="!table.getCanNextPage()"
          @click="table.setPageIndex(table.getPageCount() - 1)"
        >
          <span class="sr-only">Go to last page</span>
          <Icon icon="radix-icons:double-arrow-right" class="h-4 w-4" />
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts" generic="TData, TValue">
import type { ColumnDef, ColumnFiltersState, SortingState } from '@tanstack/vue-table'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/shared/components/ui/table'

import {
  FlexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
  getFilteredRowModel,
} from '@tanstack/vue-table'

import { ArrowUpDown, ChevronDown } from 'lucide-vue-next'
import { Icon } from '@iconify/vue'

import { h, ref, computed } from 'vue'
import { valueUpdater } from '@/shared/utils/general'

import { Input } from '@/shared/components/ui/input'
import { Button } from '@/shared/components/ui/button'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/shared/components/ui/select'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
}>()

const sorting = ref<SortingState>([])
const columnFilters = ref<ColumnFiltersState>([])

const table = useVueTable({
  get data() {
    return props.data
  },
  get columns() {
    return props.columns
  },
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  onSortingChange: updaterOrValue => valueUpdater(updaterOrValue, sorting),
  onColumnFiltersChange: updaterOrValue => valueUpdater(updaterOrValue, columnFilters),
  getFilteredRowModel: getFilteredRowModel(),
  state: {
    get sorting() {
      return sorting.value
    },
    get columnFilters() {
      return columnFilters.value
    },
  },
})

const fieldTypes = ['string', 'integer', 'number', 'boolean', 'array', 'object']
const isTypeFilterSet = computed(() =>
  columnFilters.value.some(f => f.id === 'field_type' && !!f.value)
)
</script>

<template>
  <div>
  <div class="flex flex-wrap items-center justify-between gap-4 py-4">
    <!-- Filters -->
    <div class="flex items-center gap-4 flex-nowrap">
      <!-- Name Filter -->
      <Input
        class="max-w-3xs"
        placeholder="Filter by name..."
        :model-value="table.getColumn('name')?.getFilterValue() as string"
        @update:model-value="table.getColumn('name')?.setFilterValue($event)"
      />

      <!-- Type Filter -->
      <div class="flex items-center gap-1">
        <Select
          :model-value="table.getColumn('field_type')?.getFilterValue() as string"
          @update:model-value="table.getColumn('field_type')?.setFilterValue($event)"
        >
          <SelectTrigger>
            <SelectValue class="min-w-[12ch]" placeholder="Select a type..." />
          </SelectTrigger>
          <SelectContent>
            <SelectItem v-for="type in fieldTypes" :key="type" :value="type">{{ type }}</SelectItem>
          </SelectContent>
        </Select>

        <Button
          :disabled="!isTypeFilterSet"
          variant="ghost"
          size="sm"
          @click="table.getColumn('field_type')?.setFilterValue('')"
        >
          <Icon class="h-4 w-4" icon="radix-icons:cross-2" />
          <span class="sr-only">Clear type filter</span>
        </Button>
      </div>
    </div>

    <Button as-child size="sm">
      <RouterLink to="/fields/new">
        <Icon icon="radix-icons:plus" class="h-4 w-4 mr-2" />
        Add Field
      </RouterLink>
    </Button>

  </div>

    <!-- Table -->
    <div class="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
            <TableHead v-for="header in headerGroup.headers" :key="header.id">
              <FlexRender
                v-if="!header.isPlaceholder"
                :render="header.column.columnDef.header"
                :props="header.getContext()"
              />
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <template v-if="table.getRowModel().rows?.length">
            <TableRow
              v-for="row in table.getRowModel().rows"
              :key="row.id"
              :data-state="row.getIsSelected() ? 'selected' : undefined"
            >
              <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
              </TableCell>
            </TableRow>
          </template>
          <template v-else>
            <TableRow>
              <TableCell :colspan="columns.length" class="h-24 text-center">
                No results.
              </TableCell>
            </TableRow>
          </template>
        </TableBody>
      </Table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-end space-x-2 py-4">
      <Button
        variant="outline"
        size="sm"
        :disabled="!table.getCanPreviousPage()"
        @click="table.previousPage()"
      >
        Previous
      </Button>
      <Button
        variant="outline"
        size="sm"
        :disabled="!table.getCanNextPage()"
        @click="table.nextPage()"
      >
        Next
      </Button>
    </div>
  </div>
</template>

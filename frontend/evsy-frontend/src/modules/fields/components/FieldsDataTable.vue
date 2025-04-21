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

import DataTableInputFilter from '@/shared/components/data/DataTableInputFilter.vue'
import DataTableSingleSelectFilter from '@/shared/components/data/DataTableSingleSelectFilter.vue'
import { Icon } from '@iconify/vue'

import { ref, computed } from 'vue'
import { valueUpdater } from '@/shared/utils/general'

import { Button } from '@/shared/components/ui/button'
import DataTablePagination from '@/shared/components/data/DataTablePagination.vue'
import { FieldType } from '@/modules/fields/types'

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

const fieldTypes = Object.values(FieldType)
const isTypeFilterSet = computed(() =>
  columnFilters.value.some(f => f.id === 'field_type' && !!f.value)
)
</script>

<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-4 py-4">
      <!-- Filters -->
      <div class="flex flex-nowrap items-center gap-4">
        <!-- Name Filter -->
        <DataTableInputFilter
          class="max-w-3xs"
          :column="table.getColumn('name')!"
          placeholder="Filter by name..."
        />

        <!-- Type Filter -->
        <DataTableSingleSelectFilter
          :column="table.getColumn('field_type')!"
          placeholder="Select a type..."
          :options="fieldTypes"
          :show-clear-button="isTypeFilterSet"
        />
      </div>

      <Button as-child>
        <RouterLink to="/fields/new">
          <Icon icon="radix-icons:plus" class="mr-2 h-4 w-4" />
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

    <div class="py-4">
      <DataTablePagination :table="table" />
    </div>
  </div>
</template>

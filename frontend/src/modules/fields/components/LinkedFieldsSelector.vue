<script setup lang="ts">
import { h, computed } from 'vue'
import type { Field } from '@/modules/fields/types'
import type { ColumnDef } from '@tanstack/vue-table'
import { Checkbox } from '@/shared/ui/checkbox'
import { Input } from '@/shared/ui/input'
import { useDataTable } from '@/shared/composables/useDataTable'
import DataTable from '@/shared/components/data/DataTable.vue'
import DataTableSkeleton from '@/shared/components/skeletons/DataTableSkeleton.vue'
import CompactDataTablePagination from '@/shared/components/data/CompactDataTablePagination.vue'
import DataTableColumnHeader from '@/shared/components/data/DataTableColumnHeader.vue'

const props = defineProps<{
  fields: Field[]
  selectedIds?: number[]
  isLoading?: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle', id: number): void
  (e: 'toggleAll', ids: number[], selected: boolean): void
}>()

const safeSelectedIds = computed(() => props.selectedIds || [])

const columns = computed<ColumnDef<Field>[]>(() => [
  {
    accessorKey: 'id',
    enableHiding: false,
    meta: {
      class: 'w-[6ch] text-center',
      headerClass: 'w-[6ch] text-center',
    },
    header: ({ column }) =>
      h(DataTableColumnHeader<Field, unknown>, {
        column,
        title: 'ID',
        align: 'center',
      }),
    cell: ({ row }) => h('div', { class: 'text-center font-medium' }, row.original.id),
  },
  {
    accessorKey: 'name',
    enableHiding: false,
    header: ({ column }) => h(DataTableColumnHeader<Field, unknown>, { column, title: 'Name' }),
    cell: ({ row }) =>
      h(
        'div',
        {
          class: 'truncate whitespace-nowrap overflow-hidden text-left font-medium',
          title: row.original.name,
        },
        row.original.name
      ),
  },
  {
    id: 'selection',
    enableHiding: false,
    header: ({ table }) => {
      const rows = table.getFilteredRowModel().rows
      const allIds = rows.map(r => r.original.id)
      const isAllSelected =
        allIds.length > 0 && allIds.every(id => safeSelectedIds.value.includes(id))
      const isSomeSelected = allIds.some(id => safeSelectedIds.value.includes(id))

      return h(
        'div',
        { class: 'flex justify-end pr-6' },
        h(Checkbox, {
          modelValue: isAllSelected || (isSomeSelected && 'indeterminate'),
          'onUpdate:modelValue': (value: boolean | 'indeterminate') =>
            emit('toggleAll', allIds, value === true),
          ariaLabel: 'Select all',
        })
      )
    },
    cell: ({ row }) =>
      h(
        'div',
        { class: 'flex justify-end pr-6' },
        h(Checkbox, {
          modelValue: safeSelectedIds.value.includes(row.original.id),
          'onUpdate:modelValue': () => emit('toggle', row.original.id),
          ariaLabel: 'Select field',
        })
      ),
  },
])

const { table } = useDataTable({
  data: () => props.fields,
  columns: () => columns.value,
  defaultPageSize: 5,
})
</script>

<template>
  <div class="flex flex-col gap-3">
    <!-- Full-width Search -->
    <div class="relative w-full">
      <Input
        class="h-9 w-full"
        placeholder="Search fields..."
        :model-value="table.getColumn('name')?.getFilterValue() as string"
        @update:model-value="table.getColumn('name')?.setFilterValue($event)"
        autocomplete="off"
        name="field-search"
      />
    </div>

    <!-- Table Container -->
    <div class="rounded-md border shadow-xs">
      <DataTableSkeleton v-if="isLoading" :columns="3" :rows="5" />
      <DataTable v-else :table="table" class="border-none shadow-none" />
    </div>

    <!-- Footer with Pagination and Summary -->
    <div class="flex items-center justify-between px-1">
      <div class="text-muted-foreground text-xs font-medium">
        {{ safeSelectedIds.length }} field(s) selected
      </div>
      <CompactDataTablePagination v-if="table.getPageCount() > 1" :table="table" />
    </div>
  </div>
</template>

<script setup lang="ts" generic="TData, TValue">
import type { ColumnDef } from '@tanstack/vue-table'
import CompactDataTablePagination from '@/shared/components/data/CompactDataTablePagination.vue'
import DataTable from '@/shared/components/data/DataTable.vue'
import { useDataTable } from '@/shared/composables/useDataTable'
import DataTableLayout from '@/shared/components/data/DataTableLayout.vue'
import DataTableSkeleton from '@/shared/components/skeletons/DataTableSkeleton.vue'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  isLoading: boolean
}>()

const { table } = useDataTable(
  () => props.data,
  () => props.columns
)
</script>

<template>
  <DataTableLayout>
    <template #table>
      <DataTableSkeleton v-if="isLoading" :columns="table.getVisibleFlatColumns().length" />
      <DataTable v-else :table="table" />
    </template>
    <template #footer>
      <CompactDataTablePagination
        v-if="table.getFilteredRowModel().rows.length > table.getState().pagination.pageSize"
        :table="table"
      />
    </template>
  </DataTableLayout>
</template>

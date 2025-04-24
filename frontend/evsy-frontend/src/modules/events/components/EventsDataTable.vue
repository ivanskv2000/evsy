<script setup lang="ts" generic="TData, TValue">
import type { ColumnDef } from '@tanstack/vue-table'
import DataTableInputFilter from '@/shared/components/data/DataTableInputFilter.vue'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/components/ui/button'
import DataTablePagination from '@/shared/components/data/DataTablePagination.vue'
import DataTable from '@/shared/components/data/DataTable.vue'
import { useDataTable } from '@/shared/composables/useDataTable'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
}>()

const { table, columnFilters } = useDataTable(
  () => props.data,
  () => props.columns,
  [{ id: 'id', desc: true }]
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
      </div>

      <Button as-child>
        <RouterLink to="/events/new">
          <Icon icon="radix-icons:plus" class="mr-2 h-4 w-4" />
          Add Event
        </RouterLink>
      </Button>
    </div>

    <DataTable :table="table" />

    <div class="py-4">
      <DataTablePagination :table="table" />
    </div>
  </div>
</template>

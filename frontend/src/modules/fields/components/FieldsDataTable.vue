<script setup lang="ts" generic="TData, TValue">
import type { ColumnDef } from '@tanstack/vue-table'
import DataTableInputFilter from '@/shared/components/data/DataTableInputFilter.vue'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/ui/button'
import DataTablePagination from '@/shared/components/data/DataTablePagination.vue'
import { FieldType } from '@/modules/fields/types'
import DataTable from '@/shared/components/data/DataTable.vue'
import { useDataTable } from '@/shared/composables/useDataTable'
import DataTableLayout from '@/shared/components/data/DataTableLayout.vue'
import DataTableSkeleton from '@/shared/components/skeletons/DataTableSkeleton.vue'
import DataTableMultiSelectFilter from '@/shared/components/data/DataTableMultiSelectFilter.vue'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  isLoading: boolean
}>()

const { table } = useDataTable({
  data: () => props.data,
  columns: () => props.columns,
  defaultSorting: [{ id: 'id', desc: true }],
})

const fieldTypes = Object.values(FieldType)
</script>

<template>
  <DataTableLayout>
    <template #filters>
      <!-- Name Filter -->
      <DataTableInputFilter
        class="max-w-3xs"
        :column="table.getColumn('name')!"
        placeholder="Filter by name..."
      />

      <!-- Type Filter -->
      <DataTableMultiSelectFilter
        :column="table.getColumn('field_type')"
        title="Type"
        icon="radix-icons:code"
        :options="fieldTypes"
      />
    </template>
    <template #buttons>
      <Button as-child>
        <RouterLink to="/fields/new">
          <Icon icon="radix-icons:plus" class="mr-2 h-4 w-4" />
          Add Field
        </RouterLink>
      </Button>
    </template>
    <template #table>
      <DataTableSkeleton v-if="isLoading" :columns="table.getVisibleFlatColumns().length" />
      <DataTable v-else :table="table">
        <template #row-placeholder>
          <div class="relative">
            <div class="inline-flex size-4 h-8 w-8 items-center justify-center gap-2 p-0 px-4">
              &nbsp;
            </div>
          </div>
        </template>
      </DataTable>
    </template>
    <template #footer>
      <DataTablePagination :table="table" />
    </template>
  </DataTableLayout>
</template>

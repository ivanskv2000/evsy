<script setup lang="ts" generic="TData, TValue">
import type { ColumnDef } from '@tanstack/vue-table'
import DataTableInputFilter from '@/shared/components/data/DataTableInputFilter.vue'
import DataTableSingleSelectFilter from '@/shared/components/data/DataTableSingleSelectFilter.vue'
import { Icon } from '@iconify/vue'
import { computed } from 'vue'
import { Button } from '@/shared/ui/button'
import DataTablePagination from '@/shared/components/data/DataTablePagination.vue'
import { FieldType } from '@/modules/fields/types'
import DataTable from '@/shared/components/data/DataTable.vue'
import { useDataTable } from '@/shared/composables/useDataTable'
import DataTableLayout from '@/shared/components/data/DataTableLayout.vue'
import DataTableSkeleton from '@/shared/components/skeletons/DataTableSkeleton.vue'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  isLoading: boolean
}>()

const { table, columnFilters } = useDataTable(
  () => props.data,
  () => props.columns,
  [{ id: 'id', desc: true }]
)

const fieldTypes = Object.values(FieldType)
const isTypeFilterSet = computed(() =>
  columnFilters.value.some(f => f.id === 'field_type' && !!f.value)
)
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
      <DataTableSingleSelectFilter
        :column="table.getColumn('field_type')!"
        placeholder="Select a type..."
        :options="fieldTypes"
        :show-clear-button="isTypeFilterSet"
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
          <div class="relative"><div class='inline-flex items-center justify-center gap-2 h-8 w-8 p-0 size-4 px-4'>&nbsp;</div></div>
        </template>
      </DataTable>
    </template>
    <template #footer>
      <DataTablePagination :table="table" />
    </template>
  </DataTableLayout>
</template>

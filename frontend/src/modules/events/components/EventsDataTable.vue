<script setup lang="ts" generic="TData, TValue">
import type { ColumnDef } from '@tanstack/vue-table'
import DataTableInputFilter from '@/shared/components/data/DataTableInputFilter.vue'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/ui/button'
import DataTablePagination from '@/shared/components/data/DataTablePagination.vue'
import DataTable from '@/shared/components/data/DataTable.vue'
import DataTableLayout from '@/shared/components/data/DataTableLayout.vue'
import { useDataTableWithUrlQuery } from '@/shared/composables/useDataTableWithUrlQuery'
import DataTableSkeleton from '@/shared/components/skeletons/DataTableSkeleton.vue'
import DataTableSingleSelectFilter from '@/shared/components/data/DataTableSingleSelectFilter.vue'
import type { Tag } from '@/modules/tags/types'
import type { UrlFiltersReturn, EventsUrlFilters } from '@/shared/types/urlFilters'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
  tags: Tag[]
  isLoading: boolean
  isLoadingTags: boolean
  urlFilters: UrlFiltersReturn<EventsUrlFilters>
}>()

const { table } = useDataTableWithUrlQuery(
  {
    data: () => props.data,
    columns: () => props.columns,
    defaultSorting: [{ id: 'id', desc: true }],
  },
  props.urlFilters,
  'events'
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

      <!-- Tag Filter -->
      <DataTableSingleSelectFilter
        :column="table.getColumn('tags')"
        title="Tag"
        placeholder="Search tags..."
        icon="ph:tag"
        :options="tags.map(tag => tag.id)"
        :disabled="isLoadingTags"
      />
    </template>
    <template #buttons>
      <Button as-child>
        <RouterLink to="/events/new">
          <Icon icon="radix-icons:plus" class="mr-2 h-4 w-4" />
          Add Event
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

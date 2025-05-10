import { ref } from 'vue'
import type {
  ColumnDef,
  SortingState,
  ColumnFiltersState,
  VisibilityState,
  PaginationState,
} from '@tanstack/vue-table'
import {
  getCoreRowModel,
  getFacetedRowModel,
  getFacetedUniqueValues,
  getSortedRowModel,
  getPaginationRowModel,
  getFilteredRowModel,
  useVueTable,
} from '@tanstack/vue-table'
import { valueUpdater } from '@/shared/utils/general'

type SortingOption = {
  id: string
  desc: boolean
}

type UseDataTableOptions<TData, TValue> = {
  data: () => TData[]
  columns: () => ColumnDef<TData, TValue>[]
  defaultSorting?: SortingOption[]
  defaultPageSize?: number
}

export function useDataTable<TData, TValue>({
  data,
  columns,
  defaultSorting = [],
  defaultPageSize = 10,
}: UseDataTableOptions<TData, TValue>) {
  const sorting = ref<SortingState>(defaultSorting ?? [])
  const columnFilters = ref<ColumnFiltersState>([])
  const columnVisibility = ref<VisibilityState>({})
  const rowSelection = ref({})
  const pagination = ref<PaginationState>({
    pageIndex: 0,
    pageSize: defaultPageSize,
  })

  const table = useVueTable({
    get data() {
      return data()
    },
    get columns() {
      return columns()
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getFacetedRowModel: getFacetedRowModel(),
    getFacetedUniqueValues: getFacetedUniqueValues(),
    onSortingChange: updaterOrValue => valueUpdater(updaterOrValue, sorting),
    onColumnFiltersChange: updaterOrValue => valueUpdater(updaterOrValue, columnFilters),
    onColumnVisibilityChange: updaterOrValue => valueUpdater(updaterOrValue, columnVisibility),
    onRowSelectionChange: updaterOrValue => valueUpdater(updaterOrValue, rowSelection),
    onPaginationChange: updaterOrValue => valueUpdater(updaterOrValue, pagination),
    state: {
      get sorting() {
        return sorting.value
      },
      get columnFilters() {
        return columnFilters.value
      },
      get columnVisibility() {
        return columnVisibility.value
      },
      get rowSelection() {
        return rowSelection.value
      },
      get pagination() {
        return pagination.value
      },
    },
  })

  return {
    table,
    sorting,
    columnFilters,
    pagination,
  }
}

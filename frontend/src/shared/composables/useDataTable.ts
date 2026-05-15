import { ref, type Ref } from 'vue'
import type {
  ColumnDef,
  SortingState,
  ColumnFiltersState,
  VisibilityState,
  PaginationState,
  Updater,
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

type UseDataTableOptions<TData, TValue> = {
  data: () => TData[]
  columns: () => ColumnDef<TData, TValue>[]
  // Optional controlled state
  sorting?: Ref<SortingState>
  columnFilters?: Ref<ColumnFiltersState>
  onSortingChange?: (updater: Updater<SortingState>) => void
  onColumnFiltersChange?: (updater: Updater<ColumnFiltersState>) => void
  // Default values for internal state
  defaultSorting?: SortingState
  defaultPageSize?: number
}

export function useDataTable<TData, TValue>({
  data,
  columns,
  sorting: externalSorting,
  columnFilters: externalColumnFilters,
  onSortingChange: externalOnSortingChange,
  onColumnFiltersChange: externalOnColumnFiltersChange,
  defaultSorting = [],
  defaultPageSize = 10,
}: UseDataTableOptions<TData, TValue>) {
  // Use external state if provided, otherwise create internal state
  const internalSorting = ref<SortingState>(defaultSorting)
  const internalColumnFilters = ref<ColumnFiltersState>([])

  const sorting = externalSorting || internalSorting
  const columnFilters = externalColumnFilters || internalColumnFilters

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
    onSortingChange:
      externalOnSortingChange || (updaterOrValue => valueUpdater(updaterOrValue, internalSorting)),
    onColumnFiltersChange:
      externalOnColumnFiltersChange ||
      (updaterOrValue => valueUpdater(updaterOrValue, internalColumnFilters)),
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

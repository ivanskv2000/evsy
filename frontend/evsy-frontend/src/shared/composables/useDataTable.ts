import { ref, computed } from 'vue'
import type { ColumnDef, SortingState, ColumnFiltersState } from '@tanstack/vue-table'
import {
  getCoreRowModel,
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

export function useDataTable<TData, TValue>(
  data: () => TData[],
  columns: () => ColumnDef<TData, TValue>[],
  defaultSorting?: SortingOption[]
) {
  const sorting = ref<SortingState>(defaultSorting ?? [])
  const columnFilters = ref<ColumnFiltersState>([])

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
    onSortingChange: updaterOrValue => valueUpdater(updaterOrValue, sorting),
    onColumnFiltersChange: updaterOrValue => valueUpdater(updaterOrValue, columnFilters),
    state: {
      get sorting() {
        return sorting.value
      },
      get columnFilters() {
        return columnFilters.value
      },
    },
  })

  return {
    table,
    sorting,
    columnFilters,
  }
}

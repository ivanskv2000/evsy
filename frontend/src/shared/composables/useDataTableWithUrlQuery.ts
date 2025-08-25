import type { ColumnDef } from '@tanstack/vue-table'
import { useDataTable } from './useDataTable'
import type { UrlFiltersReturn } from '@/shared/types/urlFilters'
import { useDataTableSync, tableSyncPresets } from './useDataTableSync'

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

export type TableType = 'events' | 'fields'

export function useDataTableWithUrlQuery<TData, TValue>(
  tableOptions: UseDataTableOptions<TData, TValue>,
  /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
  urlFilters: UrlFiltersReturn<any>,
  tableType: TableType
) {
  const { table, sorting, columnFilters, pagination } = useDataTable(tableOptions)

  // Use predefined configuration for the table type
  const syncConfig = tableSyncPresets[tableType]

  // Setup synchronization using the preset configuration
  /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
  useDataTableSync(table, urlFilters, syncConfig as any)

  return {
    table,
    sorting,
    columnFilters,
    pagination,
  }
}

import { watch } from 'vue'
import type { Table } from '@tanstack/vue-table'
import type { UrlFiltersReturn } from '@/shared/types/urlFilters'

// Configuration for field synchronization
export interface FieldSyncConfig {
  columnId: string
  transform?: {
    urlToTable?: (value: unknown) => unknown
    tableToUrl?: (value: unknown) => unknown
  }
}

// Configuration for sort synchronization
export interface SortSyncConfig<T> {
  sortField: keyof T
  orderField: keyof T
  defaultSort?: { column: string; order: 'asc' | 'desc' }
}

// Complete sync configuration
/* eslint-disable-next-line @typescript-eslint/no-explicit-any */
export interface DataTableSyncConfig<T extends Record<string, any>> {
  mapping: Record<keyof T, FieldSyncConfig>
  sortConfig?: SortSyncConfig<T>
}

// Utility function to capitalize first letter
function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

// Setup synchronization for a single field
/* eslint-disable @typescript-eslint/no-explicit-any */
function setupFieldSync<T extends Record<string, any>>(
  urlField: keyof T,
  fieldConfig: FieldSyncConfig,
  table: Table<any>,
  urlFilters: UrlFiltersReturn<T>
) {
  const { columnId, transform } = fieldConfig

  // URL → Table synchronization
  watch(
    () => urlFilters.filters[urlField],
    newValue => {
      const transformedValue = transform?.urlToTable?.(newValue) ?? newValue
      table.getColumn(columnId)?.setFilterValue(transformedValue || undefined)
    },
    { immediate: true }
  )

  // Table → URL synchronization
  watch(
    () => table.getColumn(columnId)?.getFilterValue(),
    newValue => {
      const transformedValue = transform?.tableToUrl?.(newValue) ?? newValue
      const updateMethodName = `update${capitalize(String(urlField))}` as keyof UrlFiltersReturn<T>

      if (typeof urlFilters[updateMethodName] === 'function') {
        const currentValue = urlFilters.filters[urlField]
        if (transformedValue !== currentValue) {
          /* eslint-disable-next-line @typescript-eslint/no-unsafe-function-type */
          ;(urlFilters[updateMethodName] as Function)(transformedValue || '')
        }
      }
    }
  )
}
/* eslint-enable @typescript-eslint/no-explicit-any */

// Setup sort synchronization
/* eslint-disable @typescript-eslint/no-explicit-any */
function setupSortSync<T extends Record<string, any>>(
  sortConfig: SortSyncConfig<T>,
  table: Table<any>,
  urlFilters: UrlFiltersReturn<T>
) {
  const { sortField, orderField, defaultSort } = sortConfig

  // URL → Table sort synchronization
  watch(
    [() => urlFilters.filters[sortField], () => urlFilters.filters[orderField]],
    ([newSort, newOrder]) => {
      if (newSort && newOrder) {
        const currentSorting = table.getState().sorting
        const targetSorting = [{ id: String(newSort), desc: newOrder === 'desc' }]

        if (JSON.stringify(currentSorting) !== JSON.stringify(targetSorting)) {
          table.setSorting(targetSorting)
        }
      }
    },
    { immediate: true }
  )

  // Table → URL sort synchronization
  watch(
    () => table.getState().sorting,
    newSorting => {
      if (newSorting.length > 0) {
        const sort = newSorting[0]
        const newSortColumn = sort.id
        const newSortOrder = sort.desc ? 'desc' : 'asc'

        const isDefaultSort =
          defaultSort && newSortColumn === defaultSort.column && newSortOrder === defaultSort.order

        if (!isDefaultSort) {
          const currentSort = urlFilters.filters[sortField]
          const currentOrder = urlFilters.filters[orderField]

          if (newSortColumn !== currentSort || newSortOrder !== currentOrder) {
            urlFilters.updateSort?.(newSortColumn, newSortOrder)
          }
        } else if (urlFilters.filters[sortField] || urlFilters.filters[orderField]) {
          // Clear URL parameters when returning to default sort
          urlFilters.updateSort?.('', 'asc')
        }
      }
    },
    { deep: true }
  )
}
/* eslint-enable @typescript-eslint/no-explicit-any */

// Main function to setup table synchronization
/* eslint-disable @typescript-eslint/no-explicit-any */
export function useDataTableSync<T extends Record<string, any>>(
  table: Table<any>,
  urlFilters: UrlFiltersReturn<T>,
  config: DataTableSyncConfig<T>
) {
  // Setup field synchronization
  Object.entries(config.mapping).forEach(([urlField, fieldConfig]) => {
    setupFieldSync(urlField as keyof T, fieldConfig as FieldSyncConfig, table, urlFilters)
  })

  // Setup sort synchronization if configured
  if (config.sortConfig) {
    setupSortSync(config.sortConfig, table, urlFilters)
  }
}
/* eslint-enable @typescript-eslint/no-explicit-any */

// Predefined transformation functions for common use cases
export const transforms = {
  // For comma-separated strings to arrays
  stringToArray: {
    urlToTable: (value: string) => (value ? value.split(',').filter(Boolean) : undefined),
    tableToUrl: (value: string[]) => (Array.isArray(value) ? value.join(',') : ''),
  },

  // For simple string filters
  string: {
    urlToTable: (value: string) => value || undefined,
    tableToUrl: (value: string) => value || '',
  },
}

// Preset configurations for common table types
export const tableSyncPresets = {
  events: {
    mapping: {
      search: { columnId: 'name', transform: transforms.string },
      tag: { columnId: 'tags', transform: transforms.string },
    },
    sortConfig: {
      sortField: 'sort' as const,
      orderField: 'order' as const,
      defaultSort: { column: 'id', order: 'desc' as const },
    },
  },

  fields: {
    mapping: {
      search: { columnId: 'name', transform: transforms.string },
      type: { columnId: 'field_type', transform: transforms.stringToArray },
    },
    sortConfig: {
      sortField: 'sort' as const,
      orderField: 'order' as const,
      defaultSort: { column: 'id', order: 'desc' as const },
    },
  },
}

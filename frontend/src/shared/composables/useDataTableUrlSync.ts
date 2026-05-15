import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Updater, SortingState, ColumnFiltersState } from '@tanstack/vue-table'

export interface SyncConfig {
  columnFilters?: Record<string, { param: string; type?: 'string' | 'array' }> // Table Column ID -> URL Query Param Config
  sorting?: {
    sortParam: string
    orderParam: string
  }
}

export function useDataTableUrlSync(config: SyncConfig) {
  const route = useRoute()
  const router = useRouter()

  const sorting = computed<SortingState>(() => {
    if (!config.sorting) return []
    const sort = route.query[config.sorting.sortParam] as string
    const order = route.query[config.sorting.orderParam] as string
    if (sort && order) {
      return [{ id: sort, desc: order === 'desc' }]
    }
    return []
  })

  const columnFilters = computed<ColumnFiltersState>(() => {
    if (!config.columnFilters) return []
    return Object.entries(config.columnFilters)
      .map(([columnId, filterConfig]) => {
        const value = route.query[filterConfig.param]
        if (value === undefined || value === null || value === '') return null

        let filterValue: unknown = value
        if (filterConfig.type === 'array') {
          filterValue = String(value).split(',').filter(Boolean)
        }

        return {
          id: columnId,
          value: filterValue,
        }
      })
      .filter((filter): filter is { id: string; value: unknown } => filter !== null)
  })

  const onSortingChange = (updaterOrValue: Updater<SortingState>) => {
    const newSorting =
      typeof updaterOrValue === 'function' ? updaterOrValue(sorting.value) : updaterOrValue

    const query = { ...route.query }
    if (config.sorting) {
      if (newSorting.length > 0) {
        query[config.sorting.sortParam] = newSorting[0].id
        query[config.sorting.orderParam] = newSorting[0].desc ? 'desc' : 'asc'
      } else {
        delete query[config.sorting.sortParam]
        delete query[config.sorting.orderParam]
      }
    }
    router.replace({ query })
  }

  const onColumnFiltersChange = (updaterOrValue: Updater<ColumnFiltersState>) => {
    const newFilters =
      typeof updaterOrValue === 'function' ? updaterOrValue(columnFilters.value) : updaterOrValue

    const query = { ...route.query }
    if (config.columnFilters) {
      Object.values(config.columnFilters).forEach(filterConfig => {
        delete query[filterConfig.param]
      })
      newFilters.forEach(filter => {
        const filterConfig = config.columnFilters![filter.id]
        if (
          filterConfig &&
          filter.value !== undefined &&
          filter.value !== null &&
          filter.value !== ''
        ) {
          if (Array.isArray(filter.value)) {
            if (filter.value.length > 0) {
              query[filterConfig.param] = filter.value.join(',')
            }
          } else {
            query[filterConfig.param] = String(filter.value)
          }
        }
      })
    }
    router.replace({ query })
  }

  return {
    state: {
      sorting,
      columnFilters,
    },
    updaters: {
      onSortingChange,
      onColumnFiltersChange,
    },
  }
}

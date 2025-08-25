import { ref, watch, onMounted, reactive, type Ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDebounceFn } from '@vueuse/core'
import type {
  UrlFiltersConfig,
  UrlFiltersReturn,
  EventsUrlFilters,
  FieldsUrlFilters,
  TagsUrlFilters,
} from '@/shared/types/urlFilters'

// Utility function to capitalize first letter
function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1)
}

// Utility function to get default value
function getDefaultValue(filterConfig: { defaultValue?: unknown; type?: string }): unknown {
  if (filterConfig.defaultValue !== undefined) {
    return filterConfig.defaultValue
  }

  // Default values based on type
  if (filterConfig.type === 'array') return []
  if (filterConfig.type === 'boolean') return false
  return ''
}

/* eslint-disable-next-line @typescript-eslint/no-explicit-any */
export function useUrlFilters<T extends Record<string, any>>(
  config: UrlFiltersConfig<T>
): UrlFiltersReturn<T> {
  const route = useRoute()
  const router = useRouter()

  // Create reactive state for all filters using refs
  const filtersRefs: Record<string, Ref<unknown>> = {}

  // Initialize all filters with default values
  Object.keys(config).forEach(key => {
    const filterConfig = config[key as keyof T]
    filtersRefs[key] = ref(getDefaultValue(filterConfig))
  })

  // Create debounced update functions for search fields
  const debouncedUpdaters: Record<string, (value: unknown) => void> = {}
  Object.entries(config).forEach(([key, filterConfig]) => {
    if (filterConfig.debounce) {
      debouncedUpdaters[key] = useDebounceFn((value: unknown) => {
        updateUrl({ [filterConfig.param]: value } as Record<
          string,
          string | string[] | boolean | null
        >)
      }, filterConfig.debounce)
    }
  })

  // Initialize filters from URL on mount
  const initializeFromUrl = () => {
    Object.entries(config).forEach(([key, filterConfig]) => {
      const urlValue = route.query[filterConfig.param] as string
      if (urlValue) {
        if (filterConfig.type === 'array') {
          filtersRefs[key].value = urlValue.split(',')
        } else if (filterConfig.type === 'boolean') {
          filtersRefs[key].value = urlValue === 'true'
        } else {
          filtersRefs[key].value = urlValue
        }
      }
    })
  }

  // Update URL with new query parameters
  const updateUrl = (newQuery: Record<string, string | string[] | boolean | null>) => {
    const currentQuery = { ...route.query }

    Object.entries(newQuery).forEach(([param, value]) => {
      if (
        value === null ||
        value === '' ||
        value === false ||
        (Array.isArray(value) && value.length === 0)
      ) {
        delete currentQuery[param]
      } else if (Array.isArray(value)) {
        currentQuery[param] = value.join(',')
      } else {
        currentQuery[param] = String(value)
      }
    })

    const currentQueryStr = JSON.stringify(route.query)
    const newQueryStr = JSON.stringify(currentQuery)

    if (currentQueryStr !== newQueryStr) {
      router.replace({
        path: route.path,
        query: currentQuery,
      })
    }
  }

  /* eslint-disable-next-line @typescript-eslint/no-unsafe-function-type */
  const updateMethods: Record<string, Function> = {}

  Object.entries(config).forEach(([key, filterConfig]) => {
    const methodName = `update${capitalize(key)}`

    if (filterConfig.debounce) {
      // For debounced fields (like search)
      updateMethods[methodName] = (value: unknown) => {
        filtersRefs[key].value = value
        debouncedUpdaters[key](value)
      }
    } else {
      // For immediate update fields
      updateMethods[methodName] = (value: unknown) => {
        filtersRefs[key].value = value
        updateUrl({ [filterConfig.param]: value } as Record<
          string,
          string | string[] | boolean | null
        >)
      }
    }
  })

  // Special method for sort that updates both sort and order
  if ('sort' in config && 'order' in config) {
    updateMethods.updateSort = (column: string, direction: 'asc' | 'desc') => {
      filtersRefs.sort.value = column
      filtersRefs.order.value = direction

      const sortConfig = config.sort as { param: string }
      const orderConfig = config.order as { param: string }

      updateUrl({
        [sortConfig.param]: column || null,
        [orderConfig.param]: column ? direction : null,
      })
    }
  }

  // Clear all filters
  const clearFilters = () => {
    const clearQuery: Record<string, null> = {}

    Object.entries(config).forEach(([key, filterConfig]) => {
      filtersRefs[key].value = getDefaultValue(filterConfig)
      clearQuery[filterConfig.param] = null
    })

    updateUrl(clearQuery)
  }

  // Update filters method for bulk updates
  const updateFilters = (newFilters: Record<string, string | null>) => {
    updateUrl(newFilters)
  }

  // Watch for route changes to update filters
  watch(
    () => route.query,
    newQuery => {
      Object.entries(config).forEach(([key, filterConfig]) => {
        const urlValue = (newQuery[filterConfig.param] as string) || ''
        let newValue: unknown

        if (filterConfig.type === 'array') {
          newValue = urlValue ? urlValue.split(',') : []
        } else if (filterConfig.type === 'boolean') {
          newValue = urlValue === 'true'
        } else {
          newValue = urlValue
        }

        if (JSON.stringify(filtersRefs[key].value) !== JSON.stringify(newValue)) {
          filtersRefs[key].value = newValue
        }
      })
    },
    { deep: true }
  )

  onMounted(() => {
    initializeFromUrl()
  })

  // Create filters object from refs for return
  const filters = reactive({}) as T
  Object.keys(config).forEach(key => {
    Object.defineProperty(filters, key, {
      get: () => filtersRefs[key].value,
      set: value => {
        filtersRefs[key].value = value
      },
    })
  })

  return {
    filters,
    ...updateMethods,
    updateFilters,
    clearFilters,
  } as UrlFiltersReturn<T>
}

// Preset configurations for common use cases
export const eventsFiltersConfig: UrlFiltersConfig<EventsUrlFilters> = {
  search: { param: 'search', debounce: 300, defaultValue: '' },
  tag: { param: 'tag', defaultValue: '' },
  sort: { param: 'sort', defaultValue: '' },
  order: { param: 'order', defaultValue: '' },
}

export const fieldsFiltersConfig: UrlFiltersConfig<FieldsUrlFilters> = {
  search: { param: 'search', debounce: 300, defaultValue: '' },
  type: { param: 'type', defaultValue: '' },
  sort: { param: 'sort', defaultValue: '' },
  order: { param: 'order', defaultValue: '' },
}

export const tagsFiltersConfig: UrlFiltersConfig<TagsUrlFilters> = {
  search: { param: 'search', debounce: 300, defaultValue: '' },
}

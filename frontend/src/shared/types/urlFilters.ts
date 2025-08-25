// URL Filter type definitions for each page

export interface EventsUrlFilters {
  search: string
  tag: string
  sort: string
  order: 'asc' | 'desc' | ''
}

export interface FieldsUrlFilters {
  search: string
  type: string
  sort: string
  order: 'asc' | 'desc' | ''
}

export interface TagsUrlFilters {
  search: string
}

// Configuration for each filter
export interface FilterConfig<T = string> {
  param: string // URL parameter name
  debounce?: number // debounce delay for search inputs
  defaultValue?: T // default value
  type?: 'string' | 'array' | 'boolean'
}

// Configuration object for URL filters
/* eslint-disable-next-line @typescript-eslint/no-explicit-any */
export type UrlFiltersConfig<T extends Record<string, any>> = {
  [K in keyof T]: FilterConfig<T[K]>
}

// Return type for useUrlFilters
/* eslint-disable-next-line @typescript-eslint/no-explicit-any */
export interface UrlFiltersReturn<T extends Record<string, any>> {
  // All filter values as reactive refs
  filters: T
  // Update methods for each filter
  updateSearch?: (value: string) => void
  updateTag?: (value: string) => void
  updateType?: (value: string) => void
  updateSort?: (column: string, direction: 'asc' | 'desc') => void
  updateFilters?: (filters: Record<string, string | null>) => void
  clearFilters: () => void
}

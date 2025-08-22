import type { FilterFn } from '@tanstack/vue-table'
import type { Event } from '@/modules/events/types'
import type { Field } from '@/modules/fields/types'
import type { Tag } from '@/modules/tags/types'

/**
 * Universal multi-field search function for any array of objects
 * @param item The item to check
 * @param fields Array of field names to search in (supports dot notation)
 * @param searchQuery The search query string
 * @returns true if item matches the search query
 */
export function searchMultiField<T>(item: T, fields: string[], searchQuery: string): boolean {
  if (!searchQuery || typeof searchQuery !== 'string') {
    return true
  }

  const searchText = searchQuery.toLowerCase().trim()
  if (!searchText) return true

  return fields.some(field => {
    const value = getNestedValue(item, field)
    if (value === null || value === undefined) return false

    const stringValue = String(value).toLowerCase()
    return stringValue.includes(searchText)
  })
}

/**
 * Filter an array using multi-field search
 * @param data Array of items to filter
 * @param fields Array of field names to search in
 * @param searchQuery The search query string
 * @returns Filtered array
 */
export function filterMultiField<T>(data: T[], fields: string[], searchQuery: string): T[] {
  if (!searchQuery?.trim()) return data

  return data.filter(item => searchMultiField(item, fields, searchQuery))
}

/**
 * Creates a TanStack Table filter function from multi-field search
 * @param fields Array of field names to search in
 * @returns TanStack Table filter function
 */
export function createTableFilter<TData>(fields: string[]): FilterFn<TData> {
  return (row, columnId, filterValue) => {
    return searchMultiField(row.original, fields, filterValue as string)
  }
}

/**
 * Gets a nested value from an object using dot notation
 * @param obj The object to get the value from
 * @param path The path to the value (e.g., 'user.name' or 'id')
 * @returns The value at the path, or undefined if not found
 */
function getNestedValue<T>(obj: T, path: string): unknown {
  return path.split('.').reduce((current: unknown, key: string) => {
    return (current as Record<string, unknown>)?.[key]
  }, obj)
}

/**
 * Pre-configured fields for different entities
 */
export const EVENTS_SEARCH_FIELDS = ['id', 'name', 'description']
export const FIELDS_SEARCH_FIELDS = ['id', 'name', 'description']
export const TAGS_SEARCH_FIELDS = ['id', 'description']

/**
 * Pre-configured TanStack Table filters
 */
export const eventsTableFilter = createTableFilter<Event>(EVENTS_SEARCH_FIELDS)
export const fieldsTableFilter = createTableFilter<Field>(FIELDS_SEARCH_FIELDS)
export const tagsTableFilter = createTableFilter<Tag>(TAGS_SEARCH_FIELDS)

/**
 * Pre-configured array filter functions
 */
export const filterEvents = (data: Event[], searchQuery: string): Event[] =>
  filterMultiField(data, EVENTS_SEARCH_FIELDS, searchQuery)

export const filterFields = (data: Field[], searchQuery: string): Field[] =>
  filterMultiField(data, FIELDS_SEARCH_FIELDS, searchQuery)

export const filterTags = (data: Tag[], searchQuery: string): Tag[] =>
  filterMultiField(data, TAGS_SEARCH_FIELDS, searchQuery)

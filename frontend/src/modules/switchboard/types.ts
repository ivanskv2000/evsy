import type { EventLink } from '@/modules/events/types'

export interface ImportBundle {
  tags: {
    id: string
    description?: string | null
  }[]

  fields: {
    name: string
    description?: string | null
    field_type: string // could use enum if available
    example?: unknown
  }[]

  events: {
    name: string
    description?: string | null
    links?: EventLink[]
    tags: string[]
    fields: string[] // field names
  }[]
}
export type ImportSource = 'json' | 'csv'

export type ExportBundle = ImportBundle
export type ExportTarget = 'json' | 'csv' | 'markdown'

export interface ResetPreview {
  would_delete: {
    events: number
    fields: number
    tags: number
  }
}

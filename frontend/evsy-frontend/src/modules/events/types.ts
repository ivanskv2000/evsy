import type { Tag } from '@/modules/tags/types'
import type { Field } from '@/modules/fields/types'

export type Event = {
  id: number
  name: string
  description?: string | null
  tags: Tag[]
  fields: Field[]
  created_at: string
  updated_at: string
} 
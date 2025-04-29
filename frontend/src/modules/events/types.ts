import type { Tag } from '@/modules/tags/types'
import type { Field } from '@/modules/fields/types'

export enum EventLinkType {
  Figma = 'figma',
  Miro = 'miro',
  Confluence = 'confluence',
  Notion = 'notion',
  Loom = 'loom',
  Slack = 'slack',
  Google = 'google',
  Other = 'other',
}

export type EventLink = {
  type: EventLinkType
  url: string
  label?: string
}

export type Event = {
  id: number
  name: string
  description?: string | null
  links?: EventLink[]
  tags: Tag[]
  fields: Field[]
  created_at: string
  updated_at: string
}

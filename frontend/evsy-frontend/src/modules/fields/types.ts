export type Field = {
  id: number
  name: string
  description?: string | null
  field_type: string // можно заменить на enum позже
  created_at: string
  updated_at: string
} 
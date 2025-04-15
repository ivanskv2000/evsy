export type Tag = {
    id: string
    description?: string | null
    created_at: string
    updated_at: string
  }
  
  export type Field = {
    id: number
    name: string
    description?: string | null
    field_type: string // можно заменить на enum позже
    created_at: string
    updated_at: string
  }
  
  export type Event = {
    id: number
    name: string
    description?: string | null
    tags: Tag[]
    fields: Field[]
    created_at: string
    updated_at: string
  }
  
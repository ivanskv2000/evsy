export enum FieldType {
  TEXT = 'text',
  NUMBER = 'number',
  DATE = 'date',
  BOOLEAN = 'boolean',
  SELECT = 'select',
}

export type Field = {
  id: number
  name: string
  description?: string | null
  field_type: FieldType
  created_at: string
  updated_at: string
}

export type FieldFormData = Omit<Field, 'id' | 'created_at' | 'updated_at'>

export type FieldValidationErrors = {
  name?: string[]
  description?: string[]
  field_type?: string[]
}

export type ApiResponse<T> = {
  data: T
  message?: string
  errors?: FieldValidationErrors
}

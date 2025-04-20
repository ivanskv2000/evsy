export enum FieldType {
  STRING = 'string',
  INTEGER = 'integer',
  NUMBER = 'number',
  BOOLEAN = 'boolean',
  ARRAY = 'array',
  OBJECT = 'object',
}

export type Field = {
  id: number
  name: string
  description: string | null
  field_type: FieldType
  created_at: string
  updated_at: string
}

export type FieldFormData = {
  name: string
  description?: string | null
  field_type: FieldType
}

export type FieldValidationErrors = {
  name?: string[]
  description?: string[]
  field_type?: string[]
}

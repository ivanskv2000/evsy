export enum FieldType {
  STRING = 'string',
  INTEGER = 'integer',
  NUMBER = 'number',
  BOOLEAN = 'boolean',
  ARRAY = 'array',
  OBJECT = 'object',
}

type FieldExampleMap = {
  [FieldType.STRING]: string
  [FieldType.INTEGER]: number
  [FieldType.NUMBER]: number
  [FieldType.BOOLEAN]: boolean
  [FieldType.ARRAY]: unknown[]
  [FieldType.OBJECT]: Record<string, unknown>
}

export type JsonValue =
  | string
  | number
  | boolean
  | null
  | JsonValue[]
  | { [key: string]: JsonValue }

export type Field = {
  id: number
  name: string
  description: string | null
  field_type: FieldType
  example: JsonValue
  created_at: string
  updated_at: string
  event_count?: number
}

export type FieldFormData = {
  name: string
  description?: string | null
  field_type: FieldType
  example?: FieldExampleMap[FieldType]
}

export type FieldValidationErrors = {
  name?: string[]
  description?: string[]
  field_type?: string[]
  example?: string[]
}

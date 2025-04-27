import { z } from 'zod'
import { FieldType } from '../types'

const exampleSchema = z.union([
  z.string(),
  z.number(),
  z.boolean(),
  z.array(z.any()),
  z.record(z.any()),
  z.null(),
])

export const fieldSchema = z.object({
  name: z.string().min(1, 'Name is required').max(32, 'Name must be less than 32 characters'),

  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional()
    .nullable(),

  field_type: z.nativeEnum(FieldType),

  example: z
    .custom((val) => {
      if (val === null || val === undefined) return true
      try {
        // Try to parse as JSON if it's a string
        const parsed = typeof val === 'string' ? JSON.parse(val) : val
        return true
      } catch {
        return false
      }
    }, 'Example must be valid JSON')
    .optional()
    .nullable(),
})

// Inferred TypeScript type from schema
export type FieldFormValues = z.infer<typeof fieldSchema>

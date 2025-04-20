import { z } from 'zod'

export const fieldSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
  field_type: z.enum(['string', 'integer', 'number', 'boolean', 'array', 'object']),
})

// Inferred TypeScript type from schema
export type FieldFormValues = z.infer<typeof fieldSchema>

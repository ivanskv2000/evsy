import { z } from 'zod'
import { FieldType } from '../types'

export const fieldSchema = z.object({
  name: z.string()
    .min(1, 'Name is required')
    .max(32, 'Name must be less than 32 characters'),
  
  description: z.string()
    .max(500, 'Description must be less than 500 characters')
    .optional()
    .nullable(),
  
  field_type: z.nativeEnum(FieldType),
})

// Inferred TypeScript type from schema
export type FieldFormValues = z.infer<typeof fieldSchema>

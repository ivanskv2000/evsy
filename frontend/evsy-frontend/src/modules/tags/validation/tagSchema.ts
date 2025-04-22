import { z } from 'zod'

export const tagSchema = z.object({
  id: z.string().min(1, 'Tag ID is required').max(32, 'Tag ID must be less than 32 characters'),
  
  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional()
    .nullable(),
})

// Inferred TypeScript type from schema
export type TagFormValues = z.infer<typeof tagSchema> 
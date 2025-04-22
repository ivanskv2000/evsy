import { z } from 'zod'

export const eventSchema = z.object({
  name: z
    .string()
    .min(1, 'Event name is required')
    .max(64, 'Event name must be less than 64 characters'),

  description: z
    .string()
    .max(500, 'Description must be less than 500 characters')
    .optional()
    .nullable(),
})

export type EventFormValues = z.infer<typeof eventSchema>

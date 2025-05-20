import { z } from 'zod'
import { EventLinkType } from '../types'

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

  fields: z.array(z.number()).optional().default([]),

  tags: z.array(z.string()).optional().default([]),

  links: z
    .array(
      z.object({
        type: z.nativeEnum(EventLinkType),
        url: z.string(),
        label: z.string().optional().nullable(),
      })
    )
    .superRefine((links, ctx) => {
      links.forEach((link, index) => {
        if (!link.url || link.url.trim() === '') {
          // skip: allow temporarily empty on creation
          return
        }

        try {
          new URL(link.url)
        } catch {
          ctx.addIssue({
            code: z.ZodIssueCode.custom,
            message: 'Must be a valid URL',
            path: [index, 'url'],
          })
        }
      })
    })
    .optional()
    .default([]),
})

export type EventFormValues = z.infer<typeof eventSchema>

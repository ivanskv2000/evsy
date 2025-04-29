import type { Event } from './types'
import { createCrudApi } from '@/shared/api/crudApiFactory'
import type { EventFormValues } from './validation/eventSchema'

export const eventApi = createCrudApi<Event, EventFormValues>('events')

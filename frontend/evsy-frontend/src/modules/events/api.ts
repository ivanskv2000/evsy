import type { Event } from './types'
import { createCrudApi } from '@/shared/api/crudApiFactory'

export const eventApi = createCrudApi<Event>('events')

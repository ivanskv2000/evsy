import { api } from '@/shared/utils/api'
import type { Event } from './types'
import type { EventFormValues } from './validation/eventSchema'

export const eventApi = {
  getAll(): Promise<Event[]> {
    return api.get<Event[]>('/events').then(response => response.data)
  },

  getById(id: number): Promise<Event> {
    return api.get<Event>(`/events/${id}`).then(response => response.data)
  },

  create(data: EventFormValues): Promise<Event> {
    return api.post<Event>('/events', data).then(response => response.data)
  },

  update(id: number, data: EventFormValues): Promise<Event> {
    return api.put<Event>(`/events/${id}`, data).then(response => response.data)
  },

  delete(id: number): Promise<Event> {
    return api.delete<Event>(`/events/${id}`).then(response => response.data)
  },
}

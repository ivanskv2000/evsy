import { api } from '@/shared/utils/api'
import type { Event } from './types'

export const eventApi = {
  getAll(): Promise<Event[]> {
    return api.get<Event[]>('/events').then(response => response.data)
  },
  
  getById(id: number): Promise<Event> {
    return api.get<Event>(`/events/${id}`).then(response => response.data)
  },
  
  create(data: Omit<Event, 'id'>): Promise<Event> {
    return api.post<Event>('/events', data).then(response => response.data)
  },

  update(id: number, data: Partial<Omit<Event, 'id'>>): Promise<Event> {
    return api.put<Event>(`/events/${id}`, data).then(response => response.data)
  },

  delete(id: number): Promise<Event> {
    return api.delete<Event>(`/events/${id}`).then(response => response.data)
  },
} 
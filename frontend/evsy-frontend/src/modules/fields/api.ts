import { api } from '@/shared/utils/api'
import type { Field } from './types'

export const fieldApi = {
  getAll(): Promise<Field[]> {
    return api.get<Field[]>('/fields').then(response => response.data)
  },
  
  getById(id: number): Promise<Field> {
    return api.get<Field>(`/fields/${id}`).then(response => response.data)
  },
  
  create(data: Omit<Field, 'id'>): Promise<Field> {
    return api.post<Field>('/fields', data).then(response => response.data)
  },

  update(id: number, data: Partial<Omit<Field, 'id'>>): Promise<Field> {
    return api.put<Field>(`/fields/${id}`, data).then(response => response.data)
  },

  delete(id: number): Promise<Field> {
    return api.delete<Field>(`/fields/${id}`).then(response => response.data)
  },
} 
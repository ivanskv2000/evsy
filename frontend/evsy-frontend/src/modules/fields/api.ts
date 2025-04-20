import { api } from '@/shared/utils/api'
import type { Field, FieldFormData } from './types'

export const fieldApi = {
  getAll(): Promise<Field[]> {
    return api.get<Field[]>('/fields').then(response => response.data)
  },

  getById(id: number): Promise<Field> {
    return api.get<Field>(`/fields/${id}`).then(response => response.data)
  },

  create(data: FieldFormData): Promise<Field> {
    return api.post<Field>('/fields', data).then(response => response.data)
  },

  update(id: number, data: FieldFormData): Promise<Field> {
    return api.put<Field>(`/fields/${id}`, data).then(response => response.data)
  },

  delete(id: number): Promise<Field> {
    return api.delete<Field>(`/fields/${id}`).then(response => response.data)
  },
}

import { api } from '@/shared/utils/api'
import type { Tag } from './types'

export const tagApi = {
  getAll(): Promise<Tag[]> {
    return api.get<Tag[]>('/tags').then(response => response.data)
  },

  getById(id: string): Promise<Tag> {
    return api.get<Tag>(`/tags/${id}`).then(response => response.data)
  },

  create(data: Omit<Tag, 'id'>): Promise<Tag> {
    return api.post<Tag>('/tags', data).then(response => response.data)
  },

  update(id: string, data: Partial<Omit<Tag, 'id'>>): Promise<Tag> {
    return api.put<Tag>(`/tags/${id}`, data).then(response => response.data)
  },

  delete(id: string): Promise<Tag> {
    return api.delete<Tag>(`/tags/${id}`).then(response => response.data)
  },
}

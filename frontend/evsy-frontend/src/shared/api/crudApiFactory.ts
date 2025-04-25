import { api } from '@/shared/utils/api'
import type { AxiosResponse } from 'axios'

export function createCrudApi<T>(endpoint: string) {
  return {
    getAll: () => api.get<T[]>(`/${endpoint}`).then((r: AxiosResponse<T[]>) => r.data),
    getById: (id: number | string) => api.get<T>(`/${endpoint}/${id}`).then((r: AxiosResponse<T>) => r.data),
    create: (data: Partial<T>) => api.post<T>(`/${endpoint}`, data).then((r: AxiosResponse<T>) => r.data),
    update: (id: number | string, data: Partial<T>) => api.put<T>(`/${endpoint}/${id}`, data).then((r: AxiosResponse<T>) => r.data),
    delete: (id: number | string) => api.delete<T>(`/${endpoint}/${id}`).then((r: AxiosResponse<T>) => r.data),
  }
} 
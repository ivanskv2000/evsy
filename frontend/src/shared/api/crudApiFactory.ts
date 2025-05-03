import { api } from '@/shared/utils/api'
import type { AxiosResponse } from 'axios'

export function createCrudApi<T, R = T>(endpoint: string) {
  type QueryParams = Record<string, string | number | boolean | undefined>

  return {
    getAll: (params?: QueryParams) =>
      api.get<T[]>(`/${endpoint}/`, { params }).then((r: AxiosResponse<T[]>) => r.data),

    getById: (id: number | string, params?: QueryParams) =>
      api.get<T>(`/${endpoint}/${id}`, { params }).then((r: AxiosResponse<T>) => r.data),

    create: (data: Partial<R>, params?: QueryParams) =>
      api.post<T>(`/${endpoint}/`, data, { params }).then((r: AxiosResponse<T>) => r.data),

    update: (id: number | string, data: Partial<R>, params?: QueryParams) =>
      api.put<T>(`/${endpoint}/${id}`, data, { params }).then((r: AxiosResponse<T>) => r.data),

    delete: (id: number | string, params?: QueryParams) =>
      api.delete<T>(`/${endpoint}/${id}`, { params }).then((r: AxiosResponse<T>) => r.data),
  }
}

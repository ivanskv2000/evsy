import { api } from '@/shared/utils/api'
import type { Field, FieldFormData, ApiResponse, FieldValidationErrors } from './types'

class FieldApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public errors?: FieldValidationErrors
  ) {
    super(message)
    this.name = 'FieldApiError'
  }
}

export const fieldApi = {
  async getAll(): Promise<Field[]> {
    try {
      const response = await api.get<ApiResponse<Field[]>>('/fields')
      return response.data.data
    } catch (error: any) {
      throw new FieldApiError(
        error.response?.data?.message || 'Failed to fetch fields',
        error.response?.status || 500,
        error.response?.data?.errors
      )
    }
  },

  async getById(id: number): Promise<Field> {
    try {
      const response = await api.get<ApiResponse<Field>>(`/fields/${id}`)
      return response.data.data
    } catch (error: any) {
      throw new FieldApiError(
        error.response?.data?.message || 'Failed to fetch field',
        error.response?.status || 500,
        error.response?.data?.errors
      )
    }
  },

  async create(data: FieldFormData): Promise<Field> {
    try {
      const response = await api.post<ApiResponse<Field>>('/fields', data)
      return response.data.data
    } catch (error: any) {
      throw new FieldApiError(
        error.response?.data?.message || 'Failed to create field',
        error.response?.status || 500,
        error.response?.data?.errors
      )
    }
  },

  async update(id: number, data: Partial<FieldFormData>): Promise<Field> {
    try {
      const response = await api.put<ApiResponse<Field>>(`/fields/${id}`, data)
      return response.data.data
    } catch (error: any) {
      throw new FieldApiError(
        error.response?.data?.message || 'Failed to update field',
        error.response?.status || 500,
        error.response?.data?.errors
      )
    }
  },

  async delete(id: number): Promise<void> {
    try {
      await api.delete<ApiResponse<void>>(`/fields/${id}`)
    } catch (error: any) {
      throw new FieldApiError(
        error.response?.data?.message || 'Failed to delete field',
        error.response?.status || 500,
        error.response?.data?.errors
      )
    }
  },
}

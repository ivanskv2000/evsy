import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosError } from 'axios'

// Базовая настройка клиента
const apiClient: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // TODO: вынести в .env
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Интерсептор для обработки ошибок или токенов
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error('[API ERROR]', error.response || error.message)
    // Здесь можно обрабатывать 401 / 403 / 500 и т.п.
    return Promise.reject(error)
  }
)

// Универсальные обёртки
export const api = {
  get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return apiClient.get<T>(url, config).then((res) => res.data)
  },
  post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    return apiClient.post<T>(url, data, config).then((res) => res.data)
  },
  put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    return apiClient.put<T>(url, data, config).then((res) => res.data)
  },
  delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return apiClient.delete<T>(url, config).then((res) => res.data)
  },
}

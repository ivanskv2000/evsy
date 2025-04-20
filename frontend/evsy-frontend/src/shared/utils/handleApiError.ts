import type { AxiosError } from 'axios'
import { useApiErrorToast } from './toast'

const { showApiErrorToast } = useApiErrorToast()

export function handleApiError(error: unknown, fallbackMessage = 'Something went wrong') {
  let message = fallbackMessage

  if (error && typeof error === 'object' && 'isAxiosError' in error) {
    const axiosError = error as AxiosError<any>
    message = axiosError.response?.data?.detail || axiosError.response?.data?.message || fallbackMessage
  }

  // Show toast error
  showApiErrorToast(error, message)

  console.error('[API ERROR]', error)
}

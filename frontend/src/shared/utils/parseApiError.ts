import { isAxiosError } from 'axios'

type ErrorResponse =
  | {
      detail?: string | { msg: string }[] | { msg?: string; type?: string }
      message?: string
      title?: string
    }
  | { [key: string]: unknown }

/**
 * Extracts a user-friendly message from an unknown error.
 * Handles Axios errors, Pydantic validation errors, network issues, and generic JS errors.
 */
export function parseApiError(error: unknown, fallbackMessage = 'Something went wrong'): string {
  if (isAxiosError<ErrorResponse>(error)) {
    const status = error.response?.status

    if (!error.response) {
      return 'Network error: Failed to connect to server'
    }

    const data = error.response.data

    if (typeof data?.detail === 'string') {
      return `${status ?? ''} ${data.detail}`
    } else if (Array.isArray(data?.detail)) {
      const firstError = data.detail[0]
      return `${status ?? ''} ${firstError?.msg ?? fallbackMessage}`
    } else if (data?.message) {
      return `${status ?? ''} ${data.message}`
    } else if (data?.title) {
      return `${status ?? ''} ${data.title}`
    } else if (
      data?.detail &&
      typeof data.detail === 'object' &&
      'msg' in data.detail &&
      typeof data.detail.msg === 'string'
    ) {
      return `${status ?? ''} ${data.detail.msg}`
    }
  } else if (error instanceof Error) {
    return error.message
  }

  return fallbackMessage
}

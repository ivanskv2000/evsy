import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { isAxiosError } from 'axios'

type ErrorResponse =
  | { detail?: string | { msg: string }[]; message?: string }
  | { [key: string]: unknown }

export function useEnhancedToast() {
  const { showApiErrorToast } = useApiErrorToast()
  const { showSuccessToast } = useSuccessToast()
  const { showInfoToast } = useInfoToast()

  return {
    // Success messages
    showSuccess: (message: string) => showSuccessToast(message),
    showCreated: (entity: string) => showSuccessToast(`${entity} created successfully!`),
    showUpdated: (entity: string) => showSuccessToast(`${entity} updated successfully!`),
    showDeleted: (entity: string) => showSuccessToast(`${entity} deleted successfully!`),

    // Info messages
    showInfo: (message: string) => showInfoToast(message),
    showCopied: (item: string) => showInfoToast(`${item} copied to clipboard`),

    // Error handling
    showError: (error: unknown, fallbackMessage = 'Something went wrong') => {
      let message = fallbackMessage

      if (isAxiosError<ErrorResponse>(error)) {
        const status = error.response?.status
        const data = error.response?.data

        if (typeof data?.detail === 'string') {
          message = `${status ?? ''} ${data.detail}`
        } else if (Array.isArray(data?.detail)) {
          // Pydantic validation errors
          const firstError = data.detail[0]
          message = `${status ?? ''} ${firstError?.msg ?? fallbackMessage}`
        } else if (data?.message) {
          message = `${status ?? ''} ${data.message}`
        }
      }

      showApiErrorToast(message)

      if (import.meta.env.DEV) {
        console.error('[API ERROR]', error)
      }
    },

    // Common error messages
    showCopyError: (item: string) => showApiErrorToast(`Failed to copy ${item}`),
    showDeleteError: (entity: string) => showApiErrorToast(`Failed to delete ${entity}`),
    showUpdateError: (entity: string) => showApiErrorToast(`Failed to update ${entity}`),
    showCreateError: (entity: string) => showApiErrorToast(`Failed to create ${entity}`),
  }
}

import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import type { AxiosError } from 'axios'

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

      if (error && typeof error === 'object' && 'isAxiosError' in error) {
        const axiosError = error as AxiosError<any>
        message = axiosError.response?.data?.detail || axiosError.response?.data?.message || fallbackMessage
      }

      showApiErrorToast(error, message)
      console.error('[API ERROR]', error)
    },

    // Common error messages
    showCopyError: (item: string) => showApiErrorToast(`Failed to copy ${item}`),
    showDeleteError: (entity: string) => showApiErrorToast(`Failed to delete ${entity}`),
    showUpdateError: (entity: string) => showApiErrorToast(`Failed to update ${entity}`),
    showCreateError: (entity: string) => showApiErrorToast(`Failed to create ${entity}`),
  }
} 
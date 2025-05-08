import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { parseApiError } from '@/shared/utils/parseApiError'

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
      const message = parseApiError(error, fallbackMessage)
      showApiErrorToast(message)

      if (import.meta.env.VITE_ENV === 'dev') {
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

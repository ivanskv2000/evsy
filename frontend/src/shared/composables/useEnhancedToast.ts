import { toast } from 'vue-sonner'
import { parseApiError } from '@/shared/utils/parseApiError'

/**
 * A composable that provides enhanced toast notifications,
 * including automatic API error parsing.
 */
export function useEnhancedToast() {
  /**
   * Shows an error toast. If the error is from an API call,
   * it will be parsed into a user-friendly message.
   * @param error The error object (can be of unknown type).
   * @param title The title for the toast.
   */
  function showError(error: unknown, title = 'An Error Occurred') {
    const description = parseApiError(error)
    toast.error(title, {
      description,
      duration: 5000, // Give users a bit more time to read errors
    })
  }

  /**
   * Shows a success toast.
   * @param title The title for the toast.
   * @param description Optional description.
   */
  function showSuccess(title = 'Success', description?: string) {
    toast.success(title, {
      description,
      duration: 3000,
    })
  }

  /**
   * Shows an info toast.
   * @param title The title for the toast.
   * @param description Optional description.
   */
  function showInfo(title = 'Info', description?: string) {
    toast.info(title, {
      description,
      duration: 3000,
    })
  }

  return {
    showError,
    showSuccess,
    showInfo,

    // Common toasts utilities
    showCreated: (entity: string) => showSuccess(`${entity} created successfully!`),
    showUpdated: (entity: string) => showSuccess(`${entity} updated successfully!`),
    showDeleted: (entity: string) => showSuccess(`${entity} deleted successfully!`),
    showCopied: (item: string) => showInfo(`${item} copied to clipboard`),
    showCopyError: (item: string) => showInfo(`Failed to copy ${item}`),
  }
}

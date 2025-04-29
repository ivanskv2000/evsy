import type { AxiosError } from 'axios'
import { toast } from 'vue-sonner'

export function useApiErrorToast() {
  function showApiErrorToast(error: unknown, fallbackMessage = 'Something went wrong.') {
    let message = fallbackMessage
  
    if (
      typeof error === 'object' &&
      error !== null &&
      'response' in error &&
      typeof (error as AxiosError).response?.data === 'object'
    ) {
      const data = (error as AxiosError<{ detail?: string; message?: string }>).response?.data
      message = data?.detail ?? data?.message ?? fallbackMessage
    }
  
    toast.error('API Error', {
      description: message,
      duration: 3000,
    })
  }
  

  return { showApiErrorToast }
}

export function useSuccessToast(
  defaultTitle = 'Success',
  defaultDescription = 'Saved successfully'
) {
  function showSuccessToast(title?: string, description?: string) {
    toast.success(title || defaultTitle, {
      description: description || defaultDescription,
      duration: 3000,
    })
  }

  return { showSuccessToast }
}

export function useInfoToast() {
  function showInfoToast(title: string, description?: string) {
    toast.info(title, {
      description: description,
      duration: 3000,
    })
  }

  return { showInfoToast }
}

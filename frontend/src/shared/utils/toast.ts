import { toast } from 'vue-sonner'

export function useApiErrorToast() {
  function showApiErrorToast(message: string) {
    toast.error('API Error', {
      description: message,
      duration: 3000,
    })
  }

  return { showApiErrorToast }
}

export function useSuccessToast(defaultTitle = 'Success', defaultDescription = '') {
  function showSuccessToast(title?: string, description?: string) {
    toast.success(title ?? defaultTitle, {
      description: description ?? defaultDescription,
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

import { ref } from 'vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

export function useAsyncTask() {
  const isLoading = ref(false)
  const { showError } = useEnhancedToast()

  async function run<T>(
    task: () => Promise<T>,
    onSuccess?: (result: T) => void
  ): Promise<T | null> {
    isLoading.value = true
    try {
      const result = await task()
      onSuccess?.(result)
      return result
    } catch (error) {
      showError(error)
      return null
    } finally {
      isLoading.value = false
    }
  }

  return {
    isLoading,
    run,
  }
}

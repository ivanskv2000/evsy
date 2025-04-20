import { ref } from 'vue'
import { handleApiError } from '@/shared/utils/handleApiError'

export function useAsyncTask() {
  const isLoading = ref(false)

  async function run<T>(task: () => Promise<T>, onSuccess?: (result: T) => void): Promise<T | null> {
    isLoading.value = true
    try {
      const result = await task()
      onSuccess?.(result)
      return result
    } catch (error) {
      handleApiError(error)
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

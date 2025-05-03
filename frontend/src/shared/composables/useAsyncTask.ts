import { ref } from 'vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

export function useAsyncTask(minDelay = 400) {
  const isLoading = ref(false)
  const { showError } = useEnhancedToast()

  async function run<T>(
    task: () => Promise<T>,
    onSuccess?: (result: T) => void
  ): Promise<T | null> {
    isLoading.value = true
    const start = Date.now()

    try {
      const result = await task()
      onSuccess?.(result)

      const elapsed = Date.now() - start
      const remaining = minDelay - elapsed
      if (remaining > 0) {
        await new Promise(resolve => setTimeout(resolve, remaining))
      }

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

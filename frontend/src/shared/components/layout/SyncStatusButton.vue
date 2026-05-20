<script setup lang="ts">
import { ref, computed } from 'vue'
import { useIsFetching, useQueryClient, onlineManager } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/ui/button'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/shared/ui/tooltip'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

const isFetching = useIsFetching()
const queryClient = useQueryClient()
const { showSuccess, showError } = useEnhancedToast()

const isSyncing = ref(false)

// Combine TanStack's background fetching with our artificial minimum duration
const isRefreshing = computed(() => isSyncing.value || isFetching.value > 0)

const handleRefresh = async () => {
  if (isSyncing.value) return

  isSyncing.value = true

  try {
    await Promise.all([
      queryClient.invalidateQueries(),
      new Promise(resolve => setTimeout(resolve, 600)),
    ])

    if (!onlineManager.isOnline()) {
      showError(
        new Error('You are currently offline. Please check your internet connection and try again.')
      )
      return
    }

    showSuccess('Data is updated successfully!')
  } catch {
    // We don't call showError here because the globalErrorHandler in App.vue
    // is already attached to the queryCache and will handle any query-related errors.
  } finally {
    isSyncing.value = false
  }
}
</script>

<template>
  <TooltipProvider :delay-duration="150">
    <Tooltip>
      <TooltipTrigger as-child>
        <Button
          variant="ghost"
          size="icon"
          class="h-8 w-8"
          :disabled="isRefreshing"
          @click="handleRefresh"
        >
          <Icon
            icon="radix-icons:update"
            class="h-4 w-4"
            :class="{ 'animate-spin': isRefreshing }"
          />
          <span class="sr-only">Refresh data</span>
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>{{ isRefreshing ? 'Syncing data...' : 'Refresh all data' }}</p>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
</template>

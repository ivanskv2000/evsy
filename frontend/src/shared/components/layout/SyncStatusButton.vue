<script setup lang="ts">
import { useIsFetching, useQueryClient } from '@tanstack/vue-query'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/ui/button'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/shared/ui/tooltip'

const isFetching = useIsFetching()
const queryClient = useQueryClient()

const handleRefresh = () => {
  queryClient.invalidateQueries()
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
          :disabled="isFetching > 0"
          @click="handleRefresh"
        >
          <Icon v-if="isFetching > 0" icon="radix-icons:update" class="h-4 w-4 animate-spin" />
          <Icon v-else icon="radix-icons:update" class="h-4 w-4" />
          <span class="sr-only">Refresh data</span>
        </Button>
      </TooltipTrigger>
      <TooltipContent>
        <p>{{ isFetching > 0 ? 'Syncing data...' : 'Refresh all data' }}</p>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
</template>

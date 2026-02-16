<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { resetDatabase } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { ResetPreview } from '../types'
import { Badge } from '@/shared/ui/badge'
import { Icon } from '@iconify/vue'

const queryClient = useQueryClient()
const { showSuccess } = useEnhancedToast()

const {
  data: preview,
  isLoading: isFetching,
  refetch: fetchPreview
} = useQuery({
  queryKey: ['resetPreview'],
  queryFn: () => resetDatabase(true),
  select: data => (data as ResetPreview).would_delete,
})

const { mutate: handleReset, isPending: isResetting } = useMutation({
  mutationFn: () => resetDatabase(false),
  onSuccess: () => {
    showSuccess('Database reset successfully')
    queryClient.invalidateQueries()
  }
})
</script>

<template>
  <SwitchboardSection
    title="Reset database"
    description="Wipe all events, fields, and tags. Use with caution."
    :with-separator="true"
  >
    <template #default>
      <div class="flex flex-wrap items-center gap-4">
        <Button variant="destructive" :disabled="isResetting" @click="handleReset"> Reset </Button>
        <div
          class="text-muted-foreground flex flex-wrap items-center gap-2 text-xs transition-opacity duration-300"
        >
          <Badge variant="outline" class="min-w-[14ch] min-h-[1.5rem] text-center font-mono">
            <Transition name="fade-slide" mode="out-in">
              <span v-if="preview" :key="preview.events">{{ preview.events  }} events</span>
            </Transition>
          </Badge>
          <Badge variant="outline" class="min-w-[14ch] min-h-[1.5rem] text-center font-mono">
            <Transition name="fade-slide" mode="out-in">
              <span v-if="preview" :key="preview.fields">{{ preview.fields }} fields</span>
            </Transition>
          </Badge>
          <Badge variant="outline" class="min-w-[14ch] min-h-[1.5rem] text-center font-mono">
            <Transition name="fade-slide" mode="out-in">
              <span v-if="preview" :key="preview.tags">{{ preview.tags }} tags</span>
            </Transition>
          </Badge>
          <Button
            variant="ghost"
            size="icon"
            :disabled="isFetching"
            @click="fetchPreview"
            title="Refresh counts"
          >
            <Icon v-if="isFetching" icon="radix-icons:reload" class="h-4 w-4 animate-spin" />
            <Icon v-else icon="radix-icons:reload" class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </template>
  </SwitchboardSection>
</template>

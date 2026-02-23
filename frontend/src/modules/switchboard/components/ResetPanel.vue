<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { resetDatabase } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { ResetPreview } from '../types'
import { Badge } from '@/shared/ui/badge'
import { Skeleton } from '@/shared/ui/skeleton'

const queryClient = useQueryClient()
const { showSuccess } = useEnhancedToast()

const { data: preview, isLoading } = useQuery({
  queryKey: ['resetPreview'],
  queryFn: () => resetDatabase(true),
  select: data => (data as ResetPreview).would_delete,
})

const { mutate: handleReset, isPending: isResetting } = useMutation({
  mutationFn: () => resetDatabase(false),
  onSuccess: () => {
    showSuccess('Database reset successfully')
    queryClient.invalidateQueries()
  },
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
          v-if="!isLoading"
          class="flex flex-wrap items-center gap-2 transition-opacity duration-300 text-muted-foreground text-xs font-mono"
        >
          <Badge variant="outline" class="min-h-[1.5rem] min-w-[14ch] text-center">
            <Transition name="fade-slide" mode="out-in">
              <span v-if="preview" :key="preview.events">{{ preview.events }} events</span>
            </Transition>
          </Badge>

          <Badge variant="outline" class="min-h-[1.5rem] min-w-[14ch] text-center">
            <Transition name="fade-slide" mode="out-in">
              <span v-if="preview" :key="preview.fields">{{ preview.fields }} fields</span>
            </Transition>
          </Badge>

          <Badge variant="outline" class="min-h-[1.5rem] min-w-[14ch] text-center">
            <Transition name="fade-slide" mode="out-in">
              <span v-if="preview" :key="preview.tags">{{ preview.tags }} tags</span>
            </Transition>
          </Badge>
        </div>
        <div
          v-if="isLoading"
          class="flex flex-wrap items-center gap-2 transition-opacity duration-300 text-muted-foreground text-xs font-mono"
        >
          <Skeleton class="h-[1.5rem] w-[14ch] rounded-md" />
          <Skeleton class="h-[1.5rem] w-[14ch] rounded-md" />
          <Skeleton class="h-[1.5rem] w-[14ch] rounded-md" />
        </div>
      </div>
    </template>
  </SwitchboardSection>
</template>
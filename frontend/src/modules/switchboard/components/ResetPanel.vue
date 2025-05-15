<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { ref, onMounted } from 'vue'
import { resetDatabase } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { ResetPreview } from '../types'
import { Badge } from '@/shared/ui/badge'
import { Icon } from '@iconify/vue'

const preview = ref<{ events: number; fields: number; tags: number } | null>(null)

const { run: runResetTask, isLoading: isResetting } = useAsyncTask()
const { run: runFetchTask, isLoading: isFetching } = useAsyncTask()

const { showSuccess } = useEnhancedToast()

const fetchPreview = () => {
  runFetchTask(
    () => resetDatabase(true),
    result => {
      if (result) preview.value = (result as ResetPreview).would_delete
    }
  )
}

const handleReset = () => {
  runResetTask(async () => {
    await resetDatabase(false)
    fetchPreview()
    showSuccess('Database reset successfully')
  })
}

onMounted(fetchPreview)
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
          v-if="preview"
          class="text-muted-foreground flex flex-wrap items-center gap-2 text-xs transition-opacity duration-300"
        >
          <Badge variant="outline" class="font-mono text-center min-w-[14ch]">
            <Transition name="fade-slide" mode="out-in">
              <span :key="preview.events">{{ preview.events }} events</span>
            </Transition>
          </Badge>
          <Badge variant="outline" class="font-mono text-center min-w-[14ch]">
            <Transition name="fade-slide" mode="out-in">
              <span :key="preview.fields">{{ preview.fields }} fields</span>
            </Transition>
          </Badge>
          <Badge variant="outline" class="font-mono text-center min-w-[14ch]">
            <Transition name="fade-slide" mode="out-in">
              <span :key="preview.tags">{{ preview.tags }} tags</span>
            </Transition>
          </Badge>
          <Button
            variant="ghost"
            size="icon"
            :disabled="isFetching"
            @click="fetchPreview"
            title="Refresh counts"
          >
            <Icon icon="radix-icons:reload" class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </template>
  </SwitchboardSection>
</template>

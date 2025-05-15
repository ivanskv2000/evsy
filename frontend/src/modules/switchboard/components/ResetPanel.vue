<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { ref, onMounted } from 'vue'
import { resetDatabase } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { ResetPreview } from '../types'

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
      <div class="space-y-4">
        <div v-if="preview" class="space-y-1 text-sm">
          <p class="font-medium">Would delete:</p>
          <ul class="ml-4 list-disc">
            <li>{{ preview.events }} events</li>
            <li>{{ preview.fields }} fields</li>
            <li>{{ preview.tags }} tags</li>
          </ul>
        </div>

        <div class="flex flex-wrap items-center gap-4">
          <Button variant="destructive" :disabled="isResetting" @click="handleReset">
            Reset
          </Button>
          <Button variant="secondary" :disabled="isFetching" @click="fetchPreview">
            Refresh preview
          </Button>
        </div>
      </div>
    </template>
  </SwitchboardSection>
</template>

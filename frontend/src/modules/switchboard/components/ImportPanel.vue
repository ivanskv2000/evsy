<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { ref } from 'vue'
import { importData } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { Input } from '@/shared/ui/input'

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)

const { run, isLoading } = useAsyncTask()
const { showSuccess } = useEnhancedToast()

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target?.files?.length) {
    selectedFile.value = target.files[0]
  }
}

const handleImport = () => {
  if (!selectedFile.value) return

  run(async () => {
    const text = await selectedFile.value!.text()
    const parsed = JSON.parse(text)
    await importData(parsed, 'json')

    showSuccess('Import successful')
    selectedFile.value = null
    fileInput.value!.value = ''
  })
}
</script>

<template>
  <SwitchboardSection
    title="Import data"
    description="Load events, fields, and tags from a JSON bundle. Works on an empty
          database only."
    :with-separator="true"
  >
    <template #default>
      <div class="flex flex-wrap items-center gap-4">
        <Input
          class="w-xs"
          type="file"
          accept="application/json"
          @change="handleFileSelect"
          ref="fileInput"
          :disabled="isLoading"
        />

        <Button :disabled="isLoading || !selectedFile" @click="handleImport"> Import </Button>
      </div>
    </template>
  </SwitchboardSection>
</template>

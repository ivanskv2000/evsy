<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { ref } from 'vue'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { importData } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Input } from '@/shared/ui/input'

const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)

const queryClient = useQueryClient()
const { showSuccess } = useEnhancedToast()

const { mutate, isPending: isLoading } = useMutation({
  mutationFn: async (file: File) => {
    const text = await file.text()
    const parsed = JSON.parse(text)
    return importData(parsed, 'json')
  },
  onSuccess: () => {
    showSuccess('Import successful')
    queryClient.invalidateQueries()
    selectedFile.value = null
    if (fileInput.value) fileInput.value.value = ''
  }
})

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target?.files?.length) {
    selectedFile.value = target.files[0]
  }
}

const handleImport = () => {
  if (!selectedFile.value) return
  mutate(selectedFile.value)
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

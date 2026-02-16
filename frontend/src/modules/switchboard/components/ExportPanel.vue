<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { ref } from 'vue'
import { useMutation } from '@tanstack/vue-query'
import { exportData } from '../api'
import { Button } from '@/shared/ui/button'
import { downloadJson } from '@/shared/utils/downloadJson'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/shared/ui/select'
import type { ExportTarget } from '../types'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

const { showSuccess } = useEnhancedToast()

const selectedFormat = ref<ExportTarget>('json')

const { mutate, isPending: isLoading } = useMutation({
  mutationFn: (format: ExportTarget) => exportData(format),
  onSuccess: (data, format) => {
    if (format === 'json') {
      downloadJson(data.data, 'evsy-export.json')
    }
    showSuccess('Exported successfully')
  }
})

const handleExport = () => {
  mutate(selectedFormat.value)
}
</script>

<template>
  <SwitchboardSection
    title="Export data"
    description="Download all events, fields, and tags in JSON format. CSV and Markdown coming soon."
    :with-separator="true"
  >
    <template #default>
      <div class="flex flex-wrap items-center gap-4">
        <Select v-model="selectedFormat">
          <SelectTrigger class="w-[200px]">
            <SelectValue placeholder="Select export type" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="json"> JSON </SelectItem>
              <SelectItem disabled value="csv"> CSV (coming soon) </SelectItem>
              <SelectItem disabled value="markdown"> Markdown (coming soon) </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>

        <Button :disabled="isLoading" @click="handleExport"> Export </Button>
      </div>
    </template>
  </SwitchboardSection>
</template>

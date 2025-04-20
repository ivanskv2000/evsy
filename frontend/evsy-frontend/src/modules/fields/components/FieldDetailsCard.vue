<script setup lang="ts">
import { ref } from 'vue'
import type { Field } from '@/modules/fields/types'
import { Button } from '@/shared/components/ui/button'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { fieldApi } from '@/modules/fields/api'

import DeleteModal from '@/shared/components/data/DeleteModal.vue'
import FieldEditModal from '@/modules/fields/components/FieldEditModal.vue'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/shared/components/ui/card'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/shared/components/ui/tooltip'
import { useRouter } from 'vue-router'
import { useClipboard } from '@vueuse/core'
import { Badge } from '@/shared/components/ui/badge'
import { Icon } from '@iconify/vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const router = useRouter()
const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()

const props = defineProps<{
  field: Field
}>()

const emit = defineEmits<{
  (e: 'updated', field: Field): void
}>()

const handleUpdate = (updatedField: Field) => {
  emit('updated', updatedField)
}

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const handleDelete = () => {
  runDeleteTask(async () => {
    await fieldApi.delete(props.field.id)
    showSuccessToast('Field deleted successfully!')
    showDeleteModal.value = false
    router.push('/fields')
  })
}

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
const { showInfoToast } = useInfoToast()

const { copy: copyId } = useClipboard({ source: props.field.id.toString() })
const { copy: copyName } = useClipboard({ source: props.field.name })

const handleCopyId = async () => {
  try {
    await copyId()
    showInfoToast('ID copied to clipboard')
  } catch (err) {
    showApiErrorToast('Failed to copy ID')
  }
}

const handleCopyName = async () => {
  try {
    await copyName()
    showInfoToast('ID copied to clipboard')
  } catch (err) {
    showApiErrorToast('Failed to copy name')
  }
}
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex items-center justify-between">
        <!-- Title & Type -->
        <div class="flex items-center space-x-2">
          <TooltipProvider :delay-duration="800">
            <Tooltip>
              <TooltipTrigger>
                <CardTitle
                  class="cursor-pointer font-mono hover:underline"
                  @click="handleCopyName"
                  >{{ field.name }}</CardTitle
                >
              </TooltipTrigger>
              <TooltipContent>
                <p>Copy</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
          <Badge variant="secondary" class="text-xs tracking-wide uppercase">{{
            field.field_type
          }}</Badge>
        </div>
        <!-- Edit & Delete -->
        <div class="flex space-x-2">
          <Button size="icon" variant="ghost" @click="showEditModal = true">
            <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
          </Button>
          <Button size="icon" variant="ghost" @click="showDeleteModal = true">
            <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
          </Button>
        </div>
      </div>

      <CardDescription v-if="field.description">{{ field.description }}</CardDescription>
    </CardHeader>

    <CardContent class="text-muted-foreground space-y-3 text-sm">
      <div class="space-y-1">
        <div
          class="hover:text-foreground flex cursor-pointer items-center gap-2"
          @click="handleCopyId"
        >
          <Icon icon="radix-icons:id-card" class="h-3 w-3" />
          <span>ID: {{ field.id }}</span>
        </div>
        <div class="flex items-center gap-2">
          <Icon icon="radix-icons:file-text" class="h-3 w-3" />
          <span>Example: <span class="font-mono">aa9d3c3404bcef58965e4bb1fe9fb23c</span></span>
          <!-- Placeholder -->
        </div>
        <div class="flex items-center gap-2">
          <Icon icon="radix-icons:bar-chart" class="h-3 w-3" />
          <span>Used in: 0 events</span>
          <!-- Placeholder -->
        </div>
      </div>
    </CardContent>

    <FieldEditModal
      v-if="showEditModal"
      :field="field"
      @close="showEditModal = false"
      @updated="handleUpdate"
    />
    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="handleDelete"
      :isDeleting="isDeleting"
      description="Once deleted, this field will be unlinked from any events it's part of."
    />
  </Card>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import type { Field } from '@/modules/fields/types'
import { Button } from '@/shared/components/ui/button'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { fieldApi } from '@/modules/fields/api'

import DeleteModal from '@/shared/components/data/DeleteModal.vue'
import FieldEditModal from '@/modules/fields/components/FieldEditModal.vue'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/shared/components/ui/card'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/shared/components/ui/tooltip'
import { useRouter } from 'vue-router'
import { useClipboard } from '@vueuse/core'
import { Badge } from '@/shared/components/ui/badge'
import { Icon } from '@iconify/vue'

const router = useRouter()
const isLoading = ref(false)

const props = defineProps<{
  field: Field
}>()

const emit = defineEmits<{
  (e: "updated", field: Field): void
}>()

const handleUpdate = (updatedField: Field) => {
  emit("updated", updatedField)
}

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const handleDelete = async () => {
    isLoading.value = true
    try {
        await fieldApi.delete(props.field.id)
        showSuccessToast("Field deleted successfully!")
        showDeleteModal.value = false
        router.push('/fields')
    } catch (err) {
        console.log(err)
        showApiErrorToast(err)
    } finally {
        isLoading.value = false
    }
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
                    <CardTitle class="font-mono cursor-pointer hover:underline" @click="handleCopyName">{{ field.name }}</CardTitle>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Copy</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
              <Badge variant="secondary" class="uppercase tracking-wide text-xs">{{ field.field_type }}</Badge>
            </div>
            <!-- Edit & Delete -->
            <div class="flex space-x-2">
              <Button size="icon" variant="ghost" @click="showEditModal = true">
                <Icon icon="radix-icons:pencil-2" class="w-4 h-4" />
              </Button>
              <Button size="icon" variant="ghost" @click="showDeleteModal = true">
                <Icon icon="radix-icons:trash" class="w-4 h-4 text-destructive" />
              </Button>
            </div>
          </div>
      
      <CardDescription v-if="field.description">{{ field.description }}</CardDescription>
    </CardHeader>

    <CardContent class="space-y-3 text-sm text-muted-foreground">
      <div class="space-y-1">
        <div class="flex items-center gap-2 cursor-pointer hover:text-foreground" @click="handleCopyId">
          <Icon icon="radix-icons:id-card" class="w-3 h-3" />
          <span>ID: {{ field.id }}</span>
        </div>
        <div class="flex items-center gap-2">
          <Icon icon="radix-icons:file-text" class="w-3 h-3" />
          <span>Example: <span class="font-mono">aa9d3c3404bcef58965e4bb1fe9fb23c</span></span> <!-- Placeholder -->
        </div>
        <div class="flex items-center gap-2">
          <Icon icon="radix-icons:bar-chart" class="w-3 h-3" />
          <span>Used in: 0 events</span> <!-- Placeholder -->
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
        description="Once deleted, this field will be unlinked from any events it's part of."
    />
  </Card>
</template>
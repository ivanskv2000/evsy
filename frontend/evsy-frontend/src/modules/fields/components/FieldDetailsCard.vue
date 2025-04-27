<script setup lang="ts">
import { ref } from 'vue'
import type { Field } from '@/modules/fields/types'
import { Button } from '@/shared/components/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import FieldEditModal from '@/modules/fields/components/FieldEditModal.vue'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
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

const router = useRouter()
const { showCopied, showCopyError } = useEnhancedToast()

const props = defineProps<{
  field: Field
  loading: {
    isSaving: boolean
    isDeleting: boolean
  }
}>()

const emit = defineEmits<{
  (e: 'update', values: FieldFormValues): void
  (e: 'delete'): void
}>()

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const submitEdit = (values: FieldFormValues) => {
  emit('update', values)
  showEditModal.value = false
}

const confirmDelete = () => {
  emit('delete')
  showDeleteModal.value = false
}

const { copy: copyId } = useClipboard({ source: props.field.id.toString() })
const { copy: copyName } = useClipboard({ source: props.field.name })

const handleCopyId = async () => {
  try {
    await copyId()
    showCopied('ID')
  } catch (err) {
    showCopyError('ID')
  }
}

const handleCopyName = async () => {
  try {
    await copyName()
    showCopied('Name')
  } catch (err) {
    showCopyError('Name')
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
                  class="cursor-pointer font-mono text-xl tracking-wide"
                  @click="handleCopyName"
                >
                  {{ field.name }}
                </CardTitle>
              </TooltipTrigger>
              <TooltipContent>
                <p>Click to copy</p>
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

      <CardDescription v-if="field.description">
        {{ field.description }}
      </CardDescription>

      <!-- Details section -->
      <div class="text-muted-foreground mt-4 space-y-3 text-sm">
        <!-- ID -->
        <div
          class="hover:text-foreground flex cursor-pointer flex-wrap items-center gap-2"
          @click="handleCopyId"
        >
          <Icon icon="radix-icons:id-card" class="h-4 w-4" />
          <span>ID: {{ field.id }}</span>
        </div>
        <!-- Example -->
        <div v-if="field.example" class="flex items-center gap-2">
          <Icon icon="radix-icons:file-text" class="h-4 w-4" />
          <span>Example: <span class="font-mono">{{ field.example }}</span></span>
        </div>
        <!-- Used in -->
        <div class="flex items-center gap-2">
          <Icon icon="radix-icons:bar-chart" class="h-4 w-4" />
          <span>Used in: 0 events</span>
        </div>
      </div>
    </CardHeader>

    <CardContent> </CardContent>

    <!-- Modals -->
    <FieldEditModal
      :open="showEditModal"
      :field="field"
      :onClose="() => (showEditModal = false)"
      :onSubmit="submitEdit"
      :isSaving="loading.isSaving"
    />
    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="confirmDelete"
      :isDeleting="loading.isDeleting"
      description="Once deleted, this field will be unlinked from any events it's part of."
    />
  </Card>
</template>

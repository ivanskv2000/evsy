<script setup lang="ts">
import { Button } from '@/shared/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/shared/components/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import type { Field } from '@/modules/fields/types'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { fieldApi } from '@/modules/fields/api'
import DeleteModal from '@/shared/components/data/DeleteModal.vue'
import FieldEditModal from '@/modules/fields/components/FieldEditModal.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()

const props = defineProps<{
  field: Field,
  handleUpdateRow: () => void,
  handleDeleteRow: () => void,
}>()

const router = useRouter()

const emit = defineEmits<{
  (e: 'updated', field: Field): void
  (e: 'deleted'): void
}>()

const handleUpdate = (updatedField: Field) => {
  emit('updated', updatedField)
  props.handleUpdateRow(updatedField)
}

const handleDelete = () => {
  runDeleteTask(async () => {
    await fieldApi.delete(props.field.id)
    showSuccessToast('Field deleted successfully!')
    showDeleteModal.value = false
    props.handleDeleteRow()
    emit('deleted')
  })
}

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
const { showInfoToast } = useInfoToast()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="h-8 w-8 p-0">
        <span class="sr-only">Open menu</span>
        <Icon icon="radix-icons:dots-horizontal" class="h-4 w-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <!-- <DropdownMenuLabel>Actions</DropdownMenuLabel> -->
      <DropdownMenuItem @click="showEditModal = true"> Edit field </DropdownMenuItem>
      <DropdownMenuItem @click="showDeleteModal = true"> Delete field </DropdownMenuItem>
      <!-- <DropdownMenuSeparator />
      <DropdownMenuItem>View customer</DropdownMenuItem>
      <DropdownMenuItem>View payment details</DropdownMenuItem> -->
    </DropdownMenuContent>
  </DropdownMenu>

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
</template>

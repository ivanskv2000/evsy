<script setup lang="ts">
import { Button } from '@/shared/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/shared/components/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import type { Field } from '@/modules/fields/types'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { fieldApi } from '@/modules/fields/api'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import FieldEditModal from '@/modules/fields/components/FieldEditModal.vue'
import { ref } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'

const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()
const { showDeleted } = useEnhancedToast()

const props = defineProps<{
  field: Field
  handleUpdateRow: (updatedField: FieldFormValues) => void
  handleDeleteRow: () => void
}>()

const handleUpdate = (updatedField: FieldFormValues) => {
  props.handleUpdateRow(updatedField)
}

const handleDelete = () => {
  runDeleteTask(async () => {
    await fieldApi.delete(props.field.id)
    showDeleted('Field')
    showDeleteModal.value = false
    props.handleDeleteRow()
  })
}

const showEditModal = ref(false)
const showDeleteModal = ref(false)
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
    :open="showEditModal"
    :field="field"
    :onClose="() => (showEditModal = false)"
    :onSubmit="handleUpdate"
  />
  <DeleteModal
    :open="showDeleteModal"
    :onClose="() => (showDeleteModal = false)"
    :onConfirm="handleDelete"
    :isDeleting="isDeleting"
    description="Once deleted, this field will be unlinked from any events it's part of."
  />
</template>

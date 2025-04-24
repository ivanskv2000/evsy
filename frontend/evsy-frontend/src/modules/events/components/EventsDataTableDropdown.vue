<script setup lang="ts">
import { Button } from '@/shared/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/shared/components/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import type { Event } from '@/modules/events/types'
import { useSuccessToast } from '@/shared/utils/toast'
import { eventApi } from '@/modules/events/api'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import EventEditModal from './EventEditModal.vue'
import { ref } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { EventFormValues } from '@/modules/events/validation/eventSchema.ts'

const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()

const props = defineProps<{
  event: Event
  handleUpdateRow: (updatedEvent: Event) => void
  handleDeleteRow: () => void
}>()

const emit = defineEmits<{
  (e: 'updated', event: Event): void
  (e: 'deleted'): void
}>()

const handleDelete = () => {
  runDeleteTask(async () => {
    await eventApi.delete(props.event.id)
    showSuccessToast('Event deleted successfully!')
    showDeleteModal.value = false
    props.handleDeleteRow()
    emit('deleted')
  })
}

const handleEditSubmit = (values: EventFormValues) => {
  runUpdateTask(
    () => eventApi.update(props.event.id, values),
    updated => {
      showSuccessToast('Event updated successfully!')
      emit('updated', updated)
      showEditModal.value = false
      props.handleUpdateRow(updated)
    }
  )
}

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { showSuccessToast } = useSuccessToast()
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
      <DropdownMenuItem @click="showEditModal = true"> Edit event </DropdownMenuItem>
      <DropdownMenuItem @click="showDeleteModal = true"> Delete event </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <EventEditModal
    :open="showEditModal"
    :event="event"
    :onClose="() => (showEditModal = false)"
    :onSubmit="handleEditSubmit"
    :isSaving="isSaving"
  />
  <DeleteModal
    :open="showDeleteModal"
    :onClose="() => (showDeleteModal = false)"
    :onConfirm="handleDelete"
    :isDeleting="isDeleting"
    description="Once deleted, this event will be unlinked from any events it's part of."
  />
</template>

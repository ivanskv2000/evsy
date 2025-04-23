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
import type { Event } from '@/modules/events/types'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { eventApi } from '@/modules/events/api'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()

const props = defineProps<{
  event: Event,
  handleUpdateRow: () => void,
  handleDeleteRow: () => void,
}>()

const router = useRouter()

const emit = defineEmits<{
  (e: 'updated', event: Event): void
  (e: 'deleted'): void
}>()

const handleUpdate = (updatedEvent: Event) => {
  emit('updated', updatedEvent)
  props.handleUpdateRow(updatedEvent)
}

const handleDelete = () => {
  runDeleteTask(async () => {
    await eventApi.delete(props.event.id)
    showSuccessToast('Event deleted successfully!')
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
      <DropdownMenuItem @click="showEditModal = true"> Edit event </DropdownMenuItem>
      <DropdownMenuItem @click="showDeleteModal = true"> Delete event </DropdownMenuItem>
      <!-- <DropdownMenuSeparator />
      <DropdownMenuItem>View customer</DropdownMenuItem>
      <DropdownMenuItem>View payment details</DropdownMenuItem> -->
    </DropdownMenuContent>
  </DropdownMenu>

  <EventEditModal
    v-if="showEditModal"
    :event="event"
    @close="showEditModal = false"
    @updated="handleUpdate"
  />
  <DeleteModal
    :open="showDeleteModal"
    :onClose="() => (showDeleteModal = false)"
    :onConfirm="handleDelete"
    description="Once deleted, this event will be unlinked from any events it's part of."
  />
</template>

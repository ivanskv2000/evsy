<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Event } from '@/modules/events/types'
import EventDetailsCard from '@/modules/events/components/EventDetailsCard.vue'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import { eventApi } from '@/modules/events/api'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

const route = useRoute()
const router = useRouter()
const event = ref<Event | null>(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { run, isLoading } = useAsyncTask()
const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()

const { showDeleted, showUpdated } = useEnhancedToast()

const handleDelete = () => {
  runDeleteTask(async () => {
    await eventApi.delete(event.value!.id)
    showDeleted('Event')
    router.push('/events')
  })
}

const handleUpdate = (values: EventFormValues) => {
  runUpdateTask(
    () => eventApi.update(event.value!.id, values),
    updated => {
      showUpdated('Event')
      event.value = updated
      showEditModal.value = false
    }
  )
}

onMounted(() => {
  const id = Number(route.params.id)
  run(
    () => eventApi.getById(id),
    result => {
      if (result) event.value = result
    }
  )
})
</script>

<template>
  <div>
    <Header title="Event details" backLink fallbackBackLink="/events" />
    <EventDetailsCard
      v-if="event"
      :event="event"
      :isLoading="isLoading"
      @edit="showEditModal = true"
      @delete="showDeleteModal = true"
    />

    <!-- Modals -->
    <EventEditModal
      :open="showEditModal"
      :event="event"
      :onClose="() => (showEditModal = false)"
      :onSubmit="handleUpdate"
      :isSaving="isSaving"
    />
    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="handleDelete"
      :isDeleting="isDeleting"
      description="Once deleted, this event will be removed permanently."
    />
  </div>
</template>

<script setup lang="ts">
import { defineAsyncComponent, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Event } from '@/modules/events/types'
import EventDetailsCard from '@/modules/events/components/EventDetailsCard.vue'
import { eventApi } from '@/modules/events/api'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import DetailsCardSkeleton from '@/shared/components/skeletons/DetailsCardSkeleton.vue'
import SwaggerExportModal from '../components/SwaggerExportModal.vue'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const EventEditModal = defineAsyncComponent(
  () => import('@/modules/events/components/EventEditModal.vue')
)

const route = useRoute()
const router = useRouter()
const event = ref<Event | null>(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showSwaggerExportModal = ref(false)

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

    <DetailsCardSkeleton v-if="isLoading || !event" />

    <EventDetailsCard
      v-else
      :event="event"
      @edit="showEditModal = true"
      @delete="showDeleteModal = true"
      @export="showSwaggerExportModal = true"
    />

    <!-- Modals -->
    <EventEditModal
      v-if="event"
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
    <SwaggerExportModal
      v-if="event"
      :open="showSwaggerExportModal"
      :onClose="() => (showSwaggerExportModal = false)"
      :eventId="event.id"
    />
  </div>
</template>

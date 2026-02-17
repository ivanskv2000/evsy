<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import EventDetailsCard from '@/modules/events/components/EventDetailsCard.vue'
import { eventApi } from '@/modules/events/api'
import Header from '@/shared/components/layout/PageHeader.vue'
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

const showEditModal = ref(false)
const showDeleteModal = ref(false)
const showSwaggerExportModal = ref(false)

const queryClient = useQueryClient()
const { showDeleted, showUpdated } = useEnhancedToast()
const eventId = Number(route.params.id)

const { data: event, isLoading } = useQuery({
  queryKey: ['events', eventId],
  queryFn: () => eventApi.getById(eventId),
})

const { mutate: deleteEvent, isPending: isDeleting } = useMutation({
  mutationFn: () => eventApi.delete(eventId),
  onSuccess: () => {
    showDeleted('Event')
    queryClient.invalidateQueries({ queryKey: ['events'] })
    router.push('/events')
  },
})

const { mutate: updateEvent, isPending: isSaving } = useMutation({
  mutationFn: (values: EventFormValues) => eventApi.update(eventId, values),
  onSuccess: () => {
    showUpdated('Event')
    queryClient.invalidateQueries({ queryKey: ['events', eventId] })
    queryClient.invalidateQueries({ queryKey: ['events'] })
    showEditModal.value = false
  },
})

const handleDelete = () => {
  deleteEvent()
}

const handleUpdate = (values: EventFormValues) => {
  updateEvent(values)
}
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

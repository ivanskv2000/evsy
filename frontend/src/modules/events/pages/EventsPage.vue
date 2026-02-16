<script setup lang="ts">
import { ref, defineAsyncComponent } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { eventApi } from '@/modules/events/api'
import { tagApi } from '@/modules/tags/api'
import type { Event } from '@/modules/events/types'
import EventsDataTable from '../components/EventsDataTable.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { getEventColumns } from '@/modules/events/components/eventColumns'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import { useUrlFilters, eventsFiltersConfig } from '@/shared/composables/useUrlFilters'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const EventEditModal = defineAsyncComponent(
  () => import('@/modules/events/components/EventEditModal.vue')
)

const queryClient = useQueryClient()
const { showUpdated, showDeleted } = useEnhancedToast()

const selectedEventId = ref<number | null>(null)
const editedEvent = ref<Event | null>(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const urlFilters = useUrlFilters(eventsFiltersConfig)

const { data: tags, isLoading: isLoadingTags } = useQuery({
  queryKey: ['tags'],
  queryFn: () => tagApi.getAll(),
})

const { data: events, isLoading } = useQuery({
  queryKey: ['events'],
  queryFn: () => eventApi.getAll(),
})

const { mutate: deleteEvent, isPending: isDeleting } = useMutation({
  mutationFn: (id: number) => eventApi.delete(id),
  onSuccess: () => {
    showDeleted('Event')
    queryClient.invalidateQueries({ queryKey: ['events'] })
  },
})

const { mutate: updateEvent, isPending: isSaving } = useMutation({
  mutationFn: (variables: { id: number; values: EventFormValues }) =>
    eventApi.update(variables.id, variables.values),
  onSuccess: () => {
    showUpdated('Event')
    queryClient.invalidateQueries({ queryKey: ['events'] })
    showEditModal.value = false
  },
})

const handleDelete = () => {
  if (!selectedEventId.value) return
  deleteEvent(selectedEventId.value)
  showDeleteModal.value = false
}

const handleUpdate = (values: EventFormValues) => {
  if (!editedEvent.value) return
  updateEvent({ id: editedEvent.value.id, values })
  showEditModal.value = false
}

const selectEditEvent = (event: Event) => {
  editedEvent.value = event
  showEditModal.value = true
}

const selectDeleteEvent = (event: Event) => {
  selectedEventId.value = event.id
  showDeleteModal.value = true
}

const columns = getEventColumns(selectEditEvent, selectDeleteEvent)

</script>

<template>
  <div>
    <Header title="Events" />
    <div class="container mx-auto">
      <EventsDataTable
        :columns="columns"
        :data="events ?? []"
        :tags="tags ?? []"
        :isLoading="isLoading"
        :isLoadingTags="isLoadingTags"
        :url-filters="urlFilters"
      />
    </div>

    <!-- Modals -->
    <EventEditModal
      v-if="editedEvent"
      :open="showEditModal"
      :event="editedEvent"
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

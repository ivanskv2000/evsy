<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { eventApi } from '@/modules/events/api'
import { tagApi } from '@/modules/tags/api'
import type { Event } from '@/modules/events/types'
import type { Tag } from '@/modules/tags/types'
import EventsDataTable from '../components/EventsDataTable.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { getEventColumns } from '@/modules/events/components/eventColumns'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'

const { run, isLoading } = useAsyncTask()
const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()
const { run: loadTags, isLoading: isLoadingTags } = useAsyncTask()
const { showUpdated, showDeleted } = useEnhancedToast()

const events = ref<Event[]>([])
const tags = ref<Tag[]>([])

const selectedEventId = ref<number | null>(null)
const editedEvent = ref<Event | null>(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const updateRow = (updated: Event) => {
  const index = events.value.findIndex(e => e.id === updated.id)
  if (index !== -1) {
    events.value = events.value.map(e => (e.id === updated.id ? updated : e))
  }
}
const deleteRow = (id: number) => {
  events.value = events.value.filter(e => e.id !== id)
}

const handleDelete = () => {
  if (!selectedEventId.value) return

  runDeleteTask(async () => {
    await eventApi.delete(selectedEventId.value!)
    showDeleted('Event')
    deleteRow(selectedEventId.value!)
    selectedEventId.value = null
    showDeleteModal.value = false
  })
}

const handleUpdate = (values: EventFormValues) => {
  runUpdateTask(
    () => eventApi.update(editedEvent.value!.id, values),
    updated => {
      showUpdated('Event')
      updateRow(updated)
      showEditModal.value = false
    }
  )
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

onMounted(() => {
  run(
    () => eventApi.getAll(),
    data => {
      events.value = data
    }
  )
  loadTags(async () => {
    tags.value = await tagApi.getAll()
  })
})
</script>

<template>
  <div>
    <Header title="Events" />
    <div class="container mx-auto">
      <EventsDataTable
        :columns="columns"
        :data="events"
        :tags="tags"
        :isLoading="isLoading"
        :isLoadingTags="isLoadingTags"
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

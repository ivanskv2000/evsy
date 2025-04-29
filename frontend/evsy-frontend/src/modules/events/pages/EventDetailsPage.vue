<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import type { Event } from '@/modules/events/types'
import EventDetailsCard from '@/modules/events/components/EventDetailsCard.vue'
import { eventApi } from '@/modules/events/api'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { EventFormValues } from '@/modules/events/validation/eventSchema.ts'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useRouter } from 'vue-router'

const route = useRoute()
const event = ref<Event | null>(null)
const router = useRouter()

const { run } = useAsyncTask()
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
      :loading="{ isSaving, isDeleting }"
      @update="handleUpdate"
      @delete="handleDelete"
    />
  </div>
</template>

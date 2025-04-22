<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import type { Event } from '@/modules/events/types'
import EventDetailsCard from '@/modules/events/components/EventDetailsCard.vue'
import { useApiErrorToast } from '@/shared/utils/toast'
import { eventApi } from '@/modules/events/api'
import Header from '@/shared/components/layout/Header.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
const { showApiErrorToast } = useApiErrorToast()
const route = useRoute()
const event = ref<Event | null>(null)
const { run, isLoading } = useAsyncTask()

const handleUpdate = (updatedEvent: Event) => {
  event.value = updatedEvent
}

onMounted(() => {
  const id = Number(route.params.id)
  run(
    () => eventApi.getById(id),
    result => {
      if (result) event.value = result
      console.log(result)
    }
  )
})
</script>

<template>
  <div>
    <Header title="Event details" backLink="/events" />
    <EventDetailsCard v-if="event" :event="event!" @updated="handleUpdate" />
  </div>
</template>

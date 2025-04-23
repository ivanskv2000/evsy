<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { eventApi } from '@/modules/events/api'
import type { Event } from '@/modules/events/types'
import EventsDataTable from '@/modules/events/components/EventsDataTable.vue'
import Header from '@/shared/components/layout/Header.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const events = ref<Event[]>([])
import { getEventColumns } from '@/modules/events/components/eventColumns'
const updateRow = (updated: Event) => {
  const index = events.value.findIndex((e) => e.id === updated.id)
  if (index !== -1) {
    events.value = events.value.map((e) => 
      e.id === updated.id ? updated : e
    )
  }
}
const deleteRow = (id: number) => {
  events.value = events.value.filter((e) => e.id !== id)
}
const columns = getEventColumns(updateRow, deleteRow)
const { isLoading, run } = useAsyncTask()

onMounted(() => {
  run(
    () => eventApi.getAll(),
    data => {
      events.value = data
    }
  )
})
</script>

<template>
  <div>
    <Header title="Events" />
    <div class="container mx-auto">
      <EventsDataTable :columns="columns" :data="events" />
    </div>
  </div>
</template>

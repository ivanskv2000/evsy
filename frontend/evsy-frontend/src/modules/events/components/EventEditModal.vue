<script setup lang="ts">
import { Dialog, DialogContent, DialogTitle } from '@/shared/components/ui/dialog'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import EventForm from '@/modules/events/components/EventForm.vue'
import type { Event } from '@/modules/events/types'
import type { Field } from '@/modules/fields/types'
import { fieldApi } from '@/modules/fields/api'
import { ref, onMounted } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const props = defineProps<{
  event: Event
  open: boolean
  onClose: () => void
  onSubmit: (values: EventFormValues) => void
  isSaving?: boolean
}>()

const fields = ref<Field[]>([])
const { run: loadFields, isLoading: isLoadingFields } = useAsyncTask()

onMounted(() => {
  loadFields(async () => {
    fields.value = await fieldApi.getAll()
  })
})
</script>

<template>
  <Dialog :open="props.open" @update:open="val => !val && props.onClose()">
    <DialogContent>
      <DialogTitle>Edit Event</DialogTitle>
      <EventForm
        :event="event"
        :availableFields="fields"
        :onSubmit="props.onSubmit"
        :isLoading="props.isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

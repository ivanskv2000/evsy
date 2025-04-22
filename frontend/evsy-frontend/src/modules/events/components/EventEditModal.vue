<script setup lang="ts">
import { Dialog, DialogContent, DialogTitle } from '@/shared/components/ui/dialog'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import EventForm from '@/modules/events/components/EventForm.vue'
import type { Event } from '@/modules/events/types'

const props = defineProps<{
  event: Event
  open: boolean
  onClose: () => void
  onSubmit: (values: EventFormValues) => void
  isSaving?: boolean
}>()
</script>

<template>
  <Dialog :open="props.open" @update:open="val => !val && props.onClose()">
    <DialogContent>
      <DialogTitle>Edit Event</DialogTitle>
      <EventForm
        :event="event"
        :onSubmit="props.onSubmit"
        :isLoading="props.isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

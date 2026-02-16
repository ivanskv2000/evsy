<script setup lang="ts">
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/shared/ui/dialog'
import type { EventFormValues } from '@/modules/events/validation/eventSchema.ts'
import EventForm from './EventForm.vue'
import type { Event } from '@/modules/events/types'
import { fieldApi } from '@/modules/fields/api'
import { tagApi } from '@/modules/tags/api'
import { useQuery } from '@tanstack/vue-query'

defineProps<{
  description?: string
  event: Event
  open: boolean
  onClose: () => void
  onSubmit: (values: EventFormValues) => void
  isSaving?: boolean
}>()

const { data: fields, isLoading: isLoadingFields } = useQuery({
  queryKey: ['fields'],
  queryFn: () => fieldApi.getAll(),
})

const { data: tags, isLoading: isLoadingTags } = useQuery({
  queryKey: ['tags'],
  queryFn: () => tagApi.getAll(),
})
</script>

<template>
  <Dialog :open="open" @update:open="onClose">
    <DialogContent class="max-h-[80vh] overflow-y-auto">
      <DialogHeader>
        <DialogTitle>Edit Event</DialogTitle>
        <DialogDescription>
          {{ description }}
        </DialogDescription>
      </DialogHeader>
      <EventForm
        v-if="event"
        :event="event"
        :availableFields="fields ?? []"
        :availableTags="tags ?? []"
        :isLoadingFields="isLoadingFields"
        :isLoadingTags="isLoadingTags"
        :onSubmit="onSubmit"
        :isLoading="isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

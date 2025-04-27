<script setup lang="ts">
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/shared/components/ui/dialog'
import type { EventFormValues } from '@/modules/events/validation/eventSchema.ts'
import EventForm from './EventForm.vue'
import type { Event } from '@/modules/events/types'
import type { Field } from '@/modules/fields/types'
import { fieldApi } from '@/modules/fields/api'
import { ref, onMounted } from 'vue'
import type { Tag } from '@/modules/tags/types'
import { tagApi } from '@/modules/tags/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const props = defineProps<{
  description?: string
  event: Event
  open: boolean
  onClose: () => void
  onSubmit: (values: EventFormValues) => void
  isSaving?: boolean
}>()

const fields = ref<Field[]>([])
const tags = ref<Tag[]>([])
const { run: loadFields, isLoading: isLoadingFields } = useAsyncTask()
const { run: loadTags, isLoading: isLoadingTags } = useAsyncTask()

onMounted(() => {
  loadFields(async () => {
    fields.value = await fieldApi.getAll()
  })
  loadTags(async () => {
    tags.value = await tagApi.getAll()
  })
})
</script>

<template>
  <Dialog :open="props.open" @update:open="val => !val && props.onClose()">
    <DialogContent>
      <DialogTitle>Edit Event</DialogTitle>
      <DialogDescription>
          {{ description }}
      </DialogDescription>
      <EventForm
        :event="event"
        :availableFields="fields"
        :availableTags="tags"
        :isLoadingFields="isLoadingFields"
        :isLoadingTags="isLoadingTags"
        :onSubmit="props.onSubmit"
        :isLoading="props.isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

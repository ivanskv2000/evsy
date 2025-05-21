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
import type { Field } from '@/modules/fields/types'
import { fieldApi } from '@/modules/fields/api'
import { ref, onMounted } from 'vue'
import type { Tag } from '@/modules/tags/types'
import { tagApi } from '@/modules/tags/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

defineProps<{
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
        :availableFields="fields"
        :availableTags="tags"
        :isLoadingFields="isLoadingFields"
        :isLoadingTags="isLoadingTags"
        :onSubmit="onSubmit"
        :isLoading="isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

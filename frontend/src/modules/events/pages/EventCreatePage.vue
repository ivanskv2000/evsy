<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { eventApi } from '@/modules/events/api'
import { fieldApi } from '@/modules/fields/api'
import { tagApi } from '@/modules/tags/api'
import type { Event } from '@/modules/events/types'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import EventForm from '@/modules/events/components/EventForm.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { Card, CardContent } from '@/shared/ui/card'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

const router = useRouter()
const queryClient = useQueryClient()
const { showCreated } = useEnhancedToast()

// const isInitialLoading = ref(true)

const { data: tags, isLoading: isLoadingTags } = useQuery({
  queryKey: ['tags'],
  queryFn: () => tagApi.getAll(),
})

const { data: fields, isLoading: isLoadingFields } = useQuery({
  queryKey: ['fields'],
  queryFn: () => fieldApi.getAll(),
})

const { mutate: createEvent, isPending: isSaving } = useMutation({
  mutationFn: (values: EventFormValues) => eventApi.create(values),
  onSuccess: (createdEvent: Event) => {
    showCreated('Event')
    queryClient.invalidateQueries({ queryKey: ['events'] })
    router.push(`/events/${createdEvent.id}`)
  },
})

const onSubmit = (values: EventFormValues) => {
  createEvent(values)
}
</script>

<template>
  <div>
    <Header title="Create new event" backLink fallbackBackLink="/events" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <EventForm
          :availableFields="fields ?? []"
          :availableTags="tags ?? []"
          :isLoadingFields="isLoadingFields"
          :isLoadingTags="isLoadingTags"
          :onSubmit="onSubmit"
          :isLoading="isSaving"
          button-text="Create"
        />
      </CardContent>
    </Card>
  </div>
</template>

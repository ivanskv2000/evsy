<script setup lang="ts">
import EventForm from '@/modules/events/components/EventForm.vue'
import { useRouter } from 'vue-router'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { ref, onMounted } from 'vue'
import { eventApi } from '@/modules/events/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { EventFormValues } from '@/modules/events/validation/eventSchema.ts'
import Header from '@/shared/components/layout/PageHeader.vue'
import { Card, CardContent } from '@/shared/ui/card'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import type { Tag } from '@/modules/tags/types'
import { tagApi } from '@/modules/tags/api'

const fields = ref<Field[]>([])
const tags = ref<Tag[]>([])

const { isLoading, run } = useAsyncTask()
const { run: loadFields, isLoading: isLoadingFields } = useAsyncTask()
const { run: loadTags, isLoading: isLoadingTags } = useAsyncTask()

const { showCreated } = useEnhancedToast()
const router = useRouter()

const onSubmit = (values: EventFormValues) => {
  run(
    () => eventApi.create(values),
    created => {
      router.push(`/events/${created.id}`)
      showCreated('Event')
    }
  )
}

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
  <div>
    <Header title="Create new event" backLink fallbackBackLink="/events" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <EventForm
          :availableFields="fields"
          :availableTags="tags"
          :isLoadingFields="isLoadingFields"
          :isLoadingTags="isLoadingTags"
          :onSubmit="onSubmit"
          :isLoading="isLoading"
          button-text="Create"
        />
      </CardContent>
    </Card>
  </div>
</template>

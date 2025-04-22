<script setup lang="ts">
import * as z from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { Input } from '@/shared/components/ui/input'
import { Button } from '@/shared/components/ui/button'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
  FormDescription
} from '@/shared/components/ui/form'
import type { Event } from '@/modules/events/types'
import { computed, ref, watchEffect } from 'vue'
import { eventSchema, type EventFormValues } from '@/modules/events/validation/eventSchema'

const props = defineProps<{
  event?: Event
  onSubmit: (data: EventFormValues) => void
  buttonText?: string
  isLoading?: boolean
}>()

const { handleSubmit, values, setValues, errors } = useForm<EventFormValues>({
  validationSchema: toTypedSchema(eventSchema),
})

const disableNameField = computed(() => !!props.event)

watchEffect(() => {
  if (props.event) {
    setValues({
      name: props.event.name,
      description: props.event.description ?? '',
    })
  }
})

const onSubmit = handleSubmit(values => {
  props.onSubmit(values)
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-6">
    <!-- Event Name -->
    <FormField name="name" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Event Name</FormLabel>
        <FormControl>
          <Input
            type="text"
            placeholder="page_view"
            v-bind="componentField"
            :disabled="disableNameField"
          />
        </FormControl>
        <FormMessage />
        <FormDescription v-if="disableNameField">This field cannot be changed after creation.</FormDescription>
      </FormItem>
    </FormField>

    <!-- Description -->
    <FormField name="description" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Description</FormLabel>
        <FormControl>
          <Input type="text" placeholder="Optional description" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Button type="submit" :disabled="isLoading">{{ buttonText || 'Create Event' }}</Button>
  </form>
</template>

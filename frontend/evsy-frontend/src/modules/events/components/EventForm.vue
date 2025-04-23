<script setup lang="ts">
import * as z from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { Input } from '@/shared/components/ui/input'
import { Button } from '@/shared/components/ui/button'
// import Checkbox from '@/shared/components/ui/checkbox.vue'
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
import type { Field } from '@/modules/fields/types'
import { computed, ref, watchEffect } from 'vue'
import { eventSchema, type EventFormValues } from '@/modules/events/validation/eventSchema'

const props = defineProps<{
  event?: Event
  availableFields: Field[]
  onSubmit: (data: EventFormValues) => void
  buttonText?: string
  isLoading?: boolean
}>()

const { handleSubmit, values, setValues, setFieldValue, errors } = useForm<EventFormValues>({
  validationSchema: toTypedSchema(eventSchema),
})

function toggleFieldSelection(id: number) {
  const current = values.fields || []
  if (current.includes(id)) {
    setFieldValue('fields', current.filter(f => f !== id))
  } else {
    setFieldValue('fields', [...current, id])
  }
}

watchEffect(() => {
  if (props.event) {
    setValues({
      name: props.event.name,
      description: props.event.description ?? '',
      fields: props.event.fields?.map(f => f.id) ?? [],
    })
  }
})

const onSubmit = handleSubmit(values => {
  props.onSubmit(values)
})
</script>

<template>
  <form @submit="onSubmit" class="space-y-6 mt-2">
    <!-- Event Name -->
    <FormField name="name" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Event Name</FormLabel>
        <FormControl>
          <Input type="text" placeholder="page_view" v-bind="componentField" />
        </FormControl>
        <FormMessage />
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

    <!-- Linked Fields -->
    <FormField name="fields" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Linked Fields</FormLabel>
        <FormDescription>Choose one or more fields this event uses.</FormDescription>
        <FormControl>
      <div class="max-h-48 overflow-y-auto border rounded-md p-4 space-y-2">
        <div
          v-for="field in availableFields"
          :key="field.id"
          class="flex items-center gap-2"
        >
        <input
          type="checkbox"
          :checked="values.fields?.includes(field.id)"
          @change="() => toggleFieldSelection(field.id)"
          :id="`field-${field.id}`"
          class="form-checkbox"
        />
          <label :for="`field-${field.id}`" class="text-sm">{{ field.name }}</label>
        </div>
      </div>
    </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Button type="submit" :disabled="isLoading">{{ buttonText || 'Create Event' }}</Button>
  </form>
</template>

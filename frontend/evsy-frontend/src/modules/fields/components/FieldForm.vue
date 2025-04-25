<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { Input } from '@/shared/components/ui/input'
import { Button } from '@/shared/components/ui/button'
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/shared/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/shared/components/ui/select'
import type { Field } from '@/modules/fields/types'
import { watchEffect } from 'vue'
import { fieldSchema, type FieldFormValues } from '@/modules/fields/validation/fieldSchema'

const props = defineProps<{
  field?: Field
  onSubmit: (data: FieldFormValues) => void
  buttonText?: string
  isLoading?: boolean
}>()

const { handleSubmit, setValues } = useForm<FieldFormValues>({
  validationSchema: toTypedSchema(fieldSchema),
})

watchEffect(() => {
  if (props.field) {
    setValues({
      name: props.field.name,
      description: props.field.description ?? '',
      field_type: props.field.field_type,
    })
  }
})

const onSubmit = handleSubmit(values => {
  props.onSubmit(values)
})
</script>

<template>
  <form @submit="onSubmit" class="mt-2 space-y-6">
    <!-- Name -->
    <FormField name="name" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Name</FormLabel>
        <FormControl>
          <Input type="text" placeholder="user_id" v-bind="componentField" />
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

    <!-- Field Type -->
    <FormField name="field_type" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Field Type</FormLabel>
        <FormControl>
          <Select v-bind="componentField">
            <SelectTrigger class="min-w-[15ch]">
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="string">String</SelectItem>
              <SelectItem value="integer">Integer</SelectItem>
              <SelectItem value="number">Number</SelectItem>
              <SelectItem value="boolean">Boolean</SelectItem>
              <SelectItem value="array">Array</SelectItem>
              <SelectItem value="object">Object</SelectItem>
            </SelectContent>
          </Select>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <div class="flex justify-end">
      <Button type="submit" :disabled="isLoading">{{ buttonText || 'Create Field' }}</Button>
    </div>
  </form>
</template>

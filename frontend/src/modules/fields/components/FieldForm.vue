<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/shared/ui/form'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/ui/select'
import type { Field } from '@/modules/fields/types'
import { FieldType } from '@/modules/fields/types'
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

const fieldTypeOptions = Object.entries(FieldType).map(([key, value]) => ({
  label: key.charAt(0) + key.slice(1).toLowerCase(),
  value,
}))
</script>

<template>
  <form @submit="onSubmit" class="mt-2 space-y-6">
    <!-- Name -->
    <FormField name="name" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Name</FormLabel>
        <FormControl>
          <Input
            type="text"
            placeholder="user_id"
            autocapitalize="off"
            autocomplete="off"
            spellcheck="false"
            v-bind="componentField"
          />
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
            <SelectTrigger class="min-w-[20ch]">
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem
                v-for="option in fieldTypeOptions"
                :key="option.value"
                :value="option.value"
              >
                {{ option.label }}
              </SelectItem>
            </SelectContent>
          </Select>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <!-- Description -->
    <FormField name="description" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Description</FormLabel>
        <FormControl>
          <Input
            type="text"
            placeholder="Optional description"
            autocomplete="off"
            v-bind="componentField"
          />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <div class="flex justify-end">
      <Button type="submit" :disabled="isLoading">{{ buttonText || 'Create Field' }}</Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
  FormDescription,
} from '@/shared/ui/form'
import type { Tag } from '@/modules/tags/types'
import { computed, watchEffect } from 'vue'
import { tagSchema, type TagFormValues } from '@/modules/tags/validation/tagSchema'

const props = defineProps<{
  tag?: Tag
  onSubmit: (data: TagFormValues) => void
  buttonText?: string
  isLoading?: boolean
}>()

const { handleSubmit, setValues } = useForm<TagFormValues>({
  validationSchema: toTypedSchema(tagSchema),
})

const disableIdField = computed(() => props.tag?.id !== undefined)

watchEffect(() => {
  if (props.tag) {
    setValues({
      id: props.tag.id,
      description: props.tag.description ?? '',
    })
  }
})

const onSubmit = handleSubmit(values => {
  props.onSubmit(values)
})
</script>

<template>
  <form @submit="onSubmit" class="mt-2 space-y-6">
    <!-- Tag ID -->
    <FormField name="id" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Tag ID</FormLabel>
        <FormControl>
          <Input
            :disabled="disableIdField"
            type="text"
            placeholder="feature_login"
            v-bind="componentField"
          />
        </FormControl>
        <FormMessage />
        <FormDescription v-if="disableIdField"
          >Tag name cannot be changed after creation.</FormDescription
        >
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

    <Button type="submit" :disabled="isLoading">{{ buttonText || 'Create Tag' }}</Button>
  </form>
</template>

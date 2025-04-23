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
import type { Tag } from '@/modules/tags/types'
import { computed, ref, watchEffect } from 'vue'
import { tagSchema, type TagFormValues } from '@/modules/tags/validation/tagSchema'

const props = defineProps<{
  tag?: Tag
  onSubmit: (data: TagFormValues) => void
  buttonText?: string,
  isLoading?: boolean
}>()

const { handleSubmit, values, setValues, errors } = useForm<TagFormValues>({
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
  <form @submit="onSubmit" class="space-y-6 mt-2">
    <!-- Tag ID -->
    <FormField name="id" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Tag ID</FormLabel>
        <FormControl>
          <Input :disabled="disableIdField" type="text" placeholder="feature_login" v-bind="componentField" />
        </FormControl>
        <FormMessage />
        <FormDescription v-if="disableIdField">Tag name cannot be changed after creation.</FormDescription>
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
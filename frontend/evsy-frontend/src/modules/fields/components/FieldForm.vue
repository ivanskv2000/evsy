<script setup lang="ts">
import { z } from 'zod'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { useRouter } from 'vue-router'

import { Input } from '@/shared/components/ui/input'
import { Button } from '@/shared/components/ui/button'
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/shared/components/ui/form'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/shared/components/ui/select'
import { fieldApi } from '@/lib/api/fields'
import { toast } from '@/shared/components/ui/toast'

const router = useRouter()

const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  description: z.string().optional(),
  field_type: z.enum(['string', 'integer', 'float', 'boolean', 'array']),
})

const form = useForm({
  validationSchema: toTypedSchema(formSchema),
})

const onSubmit = form.handleSubmit(async (values) => {
  try {
    await fieldApi.create(values)
    toast.success('Field created successfully!')
    router.push('/fields')
  } catch (error) {
    toast.error('Something went wrong')
  }
})
</script>

<template>
  <Form :form="form" @submit="onSubmit" class="space-y-6">
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
            <SelectTrigger>
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="string">String</SelectItem>
              <SelectItem value="integer">Integer</SelectItem>
              <SelectItem value="float">Float</SelectItem>
              <SelectItem value="boolean">Boolean</SelectItem>
              <SelectItem value="array">Array</SelectItem>
            </SelectContent>
          </Select>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <Button type="submit">Create Field</Button>
  </Form>
</template>
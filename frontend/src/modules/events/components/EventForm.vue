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
import {
  TagsInput,
  TagsInputInput,
  TagsInputItem,
  TagsInputItemText,
  TagsInputItemDelete,
} from '@/shared/ui/tags-input'
import {
  Combobox,
  ComboboxAnchor,
  ComboboxEmpty,
  ComboboxGroup,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from '@/shared/ui/combobox'
import type { Event } from '@/modules/events/types'
import type { Field } from '@/modules/fields/types'
import type { Tag } from '@/modules/tags/types'
import { computed, ref, watchEffect } from 'vue'
import { eventSchema, type EventFormValues } from '@/modules/events/validation/eventSchema'
import { useFilter } from 'reka-ui'

const props = defineProps<{
  event?: Event
  availableFields: Field[]
  availableTags: Tag[]
  isLoadingFields?: boolean
  isLoadingTags?: boolean
  onSubmit: (data: EventFormValues) => void
  buttonText?: string
  isLoading?: boolean
}>()

const { handleSubmit, values, setValues, setFieldValue } = useForm<EventFormValues>({
  validationSchema: toTypedSchema(eventSchema),
})

function toggleFieldSelection(id: number) {
  const current = values.fields || []
  if (current.includes(id)) {
    setFieldValue(
      'fields',
      current.filter(f => f !== id)
    )
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
      tags: props.event.tags?.map(t => t.id) ?? [],
    })
  }
})

const onSubmit = handleSubmit(values => {
  props.onSubmit(values)
})

const searchTerm = ref('')
const { contains } = useFilter({ sensitivity: 'base' })
const filteredTags = computed(() => {
  const options = props.availableTags.filter(i => !values.tags.includes(i.id))
  return searchTerm.value
    ? options.filter(option => contains(option.id, searchTerm.value))
    : options
})
const open = ref(false)
function removeTag(tagId: string) {
  const current = [...values.tags]
  const updated = current.filter(t => t !== tagId)
  setFieldValue('tags', updated)
}
</script>

<template>
  <form @submit="onSubmit" class="mt-2 space-y-6">
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

    <!-- Linked Tags -->
    <FormField name="tags" v-slot="{ componentField }">
      <FormItem>
        <FormLabel>Tags</FormLabel>
        <FormControl>
          <Combobox v-model="componentField.modelValue" v-model:open="open" :ignore-filter="true">
            <ComboboxAnchor as-child>
              <TagsInput
                v-model="componentField.modelValue"
                class="border-input bg-background ring-offset-background placeholder:text-muted-foreground focus-visible:ring-ring w-full rounded-md border px-3 py-2 text-sm focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50"
              >
                <div class="flex flex-wrap items-center gap-2">
                  <TagsInputItem
                    v-for="item in componentField.modelValue"
                    :key="item"
                    :value="item"
                  >
                    <TagsInputItemText />
                    <TagsInputItemDelete @click.stop="removeTag(item)" />
                  </TagsInputItem>
                </div>

                <ComboboxInput v-model="searchTerm" as-child>
                  <TagsInputInput
                    placeholder="Tags..."
                    class="w-auto min-w-[50px] flex-1 bg-transparent p-0 text-sm focus:outline-none"
                    @keydown.enter.prevent
                  />
                </ComboboxInput>
              </TagsInput>

              <ComboboxList class="w-[--reka-popper-anchor-width] min-w-[200px]">
                <ComboboxEmpty />
                <ComboboxGroup>
                  <ComboboxItem
                    v-for="tag in filteredTags"
                    :key="tag.id"
                    :value="tag.id"
                    @select.prevent="
                      ev => {
                        if (typeof ev.detail.value === 'string') {
                          searchTerm = ''
                          componentField.modelValue.push(ev.detail.value)
                        }

                        if (filteredTags.length === 0) {
                          open = false
                        }
                      }
                    "
                  >
                    {{ tag.id }}
                  </ComboboxItem>
                </ComboboxGroup>
              </ComboboxList>
            </ComboboxAnchor>
          </Combobox>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <!-- Linked Fields -->
    <FormField name="fields">
      <FormItem>
        <FormLabel>Linked Fields</FormLabel>
        <FormDescription>Choose one or more fields this event uses.</FormDescription>
        <FormControl>
          <div class="max-h-48 space-y-2 overflow-y-auto rounded-md border p-4">
            <div v-for="field in availableFields" :key="field.id" class="flex items-center gap-2">
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

    <div class="flex justify-end">
      <Button
        type="submit"
        :disabled="isLoading"
      >
        {{ buttonText || 'Create Event' }}
      </Button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import TagScrollArea from '@/modules/tags/components/TagScrollArea.vue'
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
  // ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from '@/shared/ui/combobox'
import { ComboboxInput } from 'reka-ui'
import type { Event } from '@/modules/events/types'
import type { Field } from '@/modules/fields/types'
import type { Tag } from '@/modules/tags/types'
import { computed, ref, watchEffect } from 'vue'
import { eventSchema, type EventFormValues } from '@/modules/events/validation/eventSchema'
import { useFilter } from 'reka-ui'
import Skeleton from '@/shared/ui/skeleton/Skeleton.vue'

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

const open = ref(false)
const searchTerm = ref('')
const { contains } = useFilter({ sensitivity: 'base' })
const filteredTags = computed(() => {
  const options = props.availableTags.filter(i => !values.tags.includes(i.id))
  return searchTerm.value
    ? options.filter(option => contains(option.id, searchTerm.value))
    : options
})

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
        <FormDescription
          >Select from existing tags or create new ones by typing and pressing
          Enter.</FormDescription
        >

        <Skeleton v-if="isLoadingTags" class="h-9 w-full rounded-md" />

        <Combobox
          v-else
          v-model="componentField.modelValue"
          v-model:open="open"
          multiple
          ignore-filter
        >
          <ComboboxAnchor as-child>
            <FormControl>
              <TagsInput
                v-model="componentField.modelValue"
                class="flex h-9 w-full justify-between gap-1"
              >
                <div class="h-5 min-w-[100px] p-0">
                  <ComboboxInput v-model="searchTerm" as-child>
                    <TagsInputInput
                      class="h-auto border-none p-0"
                      placeholder="Search tags..."
                      @keydown.enter.prevent="
                        () => {
                          const tag = searchTerm.trim()
                          if (!tag || values.tags.includes(tag)) return

                          componentField.modelValue.push(tag)
                          searchTerm = ''
                        }
                      "
                    />
                  </ComboboxInput>
                </div>

                <TagScrollArea>
                  <TagsInputItem
                    v-for="item in componentField.modelValue"
                    :key="item"
                    :value="item"
                  >
                    <TagsInputItemText />
                    <TagsInputItemDelete @click.stop="removeTag(item)" />
                  </TagsInputItem>
                </TagScrollArea>
              </TagsInput>
            </FormControl>
          </ComboboxAnchor>

          <ComboboxList class="w-[--reka-popper-anchor-width] min-w-[200px]">
            <ComboboxEmpty> No tags found. </ComboboxEmpty>

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
        </Combobox>

        <FormMessage />
      </FormItem>
    </FormField>

    <!-- Linked Fields -->
    <FormField name="fields">
      <FormItem>
        <FormLabel>Linked Fields</FormLabel>
        <FormDescription>Choose one or more fields this event uses.</FormDescription>
        <FormControl>
          <div class="max-h-24 space-y-2 overflow-y-auto rounded-md border p-4">
            <template v-if="isLoadingFields">
              <Skeleton v-for="i in 4" :key="i" class="h-5 w-[70%] rounded-md" />
            </template>

            <template v-else>
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
            </template>
          </div>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>

    <div class="flex justify-end">
      <Button type="submit" :disabled="isLoading">
        {{ buttonText || 'Create Event' }}
      </Button>
    </div>
  </form>
</template>

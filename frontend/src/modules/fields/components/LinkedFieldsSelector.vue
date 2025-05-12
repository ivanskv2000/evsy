<script setup lang="ts">
import type { Field } from '@/modules/fields/types'
import Skeleton from '@/shared/ui/skeleton/Skeleton.vue'
import Checkbox from '@/shared/ui/checkbox/Checkbox.vue'

defineProps<{
  fields: Field[]
  selectedIds: number[]
  isLoading?: boolean
}>()

const emit = defineEmits<{
  (e: 'toggle', id: number): void
}>()
</script>

<template>
  <div class="max-h-24 space-y-2 overflow-y-auto rounded-md border p-4 shadow-xs">
    <template v-if="isLoading">
      <Skeleton v-for="i in 4" :key="i" class="h-5 w-[70%] rounded-md shadow-xs" />
    </template>

    <Transition name="fade" appear>
      <div v-if="!isLoading" class="space-y-2">
        <div v-for="field in fields" :key="field.id" class="flex items-center gap-2">
          <Checkbox
            :id="`field-${field.id}`"
            :model-value="selectedIds.includes(field.id)"
            @update:model-value="() => emit('toggle', field.id)"
          />
          <label
            :for="`field-${field.id}`"
            class="text-sm leading-none font-medium peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            {{ field.name }}
          </label>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import type { Field } from '@/modules/fields/types'
import Skeleton from '@/shared/ui/skeleton/Skeleton.vue'

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
      <Skeleton v-for="i in 4" :key="i" class="h-5 w-[70%] rounded-md" />
    </template>

    <Transition name="fade" appear>
      <div v-if="!isLoading">
        <div v-for="field in fields" :key="field.id" class="flex items-center gap-2">
          <input
            type="checkbox"
            :checked="selectedIds.includes(field.id)"
            @change="() => emit('toggle', field.id)"
            :id="`field-${field.id}`"
            class="form-checkbox"
          />
          <label :for="`field-${field.id}`" class="text-sm">{{ field.name }}</label>
        </div>
      </div>
    </Transition>
  </div>
</template>

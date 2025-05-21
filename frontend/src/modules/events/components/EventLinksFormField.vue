<script setup lang="ts">
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/shared/ui/select'
import { EventLinkType, type EventLink } from '@/modules/events/types'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  modelValue: EventLink[]
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', val: EventLink[]): void
}>()

function update(index: number, patch: Partial<EventLink>) {
  const updated = [...props.modelValue]
  updated[index] = { ...updated[index], ...patch }
  emit('update:modelValue', updated)
}

function addLink() {
  emit('update:modelValue', [
    ...props.modelValue,
    { type: EventLinkType.Other, url: '', label: '' },
  ])
}

function removeLink(index: number) {
  const updated = [...props.modelValue]
  updated.splice(index, 1)
  emit('update:modelValue', updated)
}
</script>

<template>
  <div class="space-y-2">
    <div
      v-for="(link, i) in modelValue"
      :key="i"
      class="grid grid-cols-[auto_2fr_1fr_auto] items-center gap-2"
    >
      <!-- Link Type -->
      <Select
        :model-value="link.type"
        @update:model-value="val => update(i, { type: val as EventLinkType })"
      >
        <SelectTrigger class="w-[90px]">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem v-for="type in Object.values(EventLinkType)" :key="type" :value="type">
            {{ type }}
          </SelectItem>
        </SelectContent>
      </Select>

      <!-- URL -->
      <Input
        type="url"
        placeholder="https://..."
        :model-value="link.url"
        @update:model-value="val => update(i, { url: String(val) })"
      />

      <!-- Label -->
      <Input
        placeholder="Label"
        :model-value="link.label"
        @update:model-value="val => update(i, { label: String(val) })"
      />

      <!-- Remove -->
      <Button
        type="button"
        variant="ghost"
        size="icon"
        class="text-muted-foreground hover:text-destructive h-8 w-8 shrink-0"
        @click="removeLink(i)"
      >
        <Icon icon="radix-icons:cross-2" class="h-4 w-4" />
      </Button>
    </div>

    <Button type="button" variant="outline" size="sm" @click="addLink">
      <Icon icon="radix-icons:plus" class="mr-1 h-4 w-4" />
      Add link
    </Button>
  </div>
</template>

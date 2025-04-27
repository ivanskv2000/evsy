<script setup lang="ts">
import { Button } from '@/shared/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/shared/components/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import type { Event } from '@/modules/events/types'

const props = defineProps<{
  event: Event
}>()

const emit = defineEmits<{
  editMe: [event: Event]
  deleteMe: [event: Event]
}>()

const handleEdit = () => {
  emit('editMe', props.event)
}

const handleDelete = () => {
  emit('deleteMe', props.event)
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="h-8 w-8 p-0">
        <span class="sr-only">Open menu</span>
        <Icon icon="radix-icons:dots-horizontal" class="h-4 w-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem @click="handleEdit"> Edit event </DropdownMenuItem>
      <DropdownMenuItem @click="handleDelete"> Delete event </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

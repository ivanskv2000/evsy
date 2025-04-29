<script setup lang="ts">
import { Button } from '@/shared/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import type { Field } from '@/modules/fields/types'

const props = defineProps<{
  field: Field
}>()

const emit = defineEmits<{
  editMe: [field: Field]
  deleteMe: [field: Field]
}>()

const handleEdit = () => {
  emit('editMe', props.field)
}

const handleDelete = () => {
  emit('deleteMe', props.field)
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
      <DropdownMenuItem @click="handleEdit"> Edit field </DropdownMenuItem>
      <DropdownMenuItem @click="handleDelete"> Delete field </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>

<script setup lang="ts">
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogFooter,
  DialogHeader,
  DialogDescription,
} from '@/shared/ui/dialog'
import { Button } from '@/shared/ui/button'

defineProps<{
  description?: string
  open: boolean
  onClose: () => void
  onConfirm: () => void
  isDeleting?: boolean
}>()
</script>

<template>
  <Dialog :open="open" @update:open="onClose">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Are you sure?</DialogTitle>
        <DialogDescription>
          {{ description }}
        </DialogDescription>
      </DialogHeader>
      <DialogFooter class="flex justify-end gap-2">
        <Button variant="secondary" @click="onClose">Cancel</Button>
        <Button variant="destructive" :disabled="isDeleting" @click="onConfirm">Delete</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

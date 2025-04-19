<script setup lang="ts">
import { ref, watch } from 'vue'
import { Dialog, DialogContent, DialogTitle, DialogFooter, DialogHeader, DialogDescription } from '@/shared/components/ui/dialog'
import { Button } from '@/shared/components/ui/button'

defineProps<{
  description: string,
  open: boolean
  onClose: () => void
  onConfirm: () => void
}>()

const isLoading = ref(false)
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
        <Button variant="destructive" @click="onConfirm">Delete</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
  
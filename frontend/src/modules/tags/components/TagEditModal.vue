<script setup lang="ts">
import { Dialog, DialogContent, DialogTitle } from '@/shared/ui/dialog'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import TagForm from '@/modules/tags/components/TagForm.vue'
import type { Tag } from '@/modules/tags/types'

const props = defineProps<{
  tag: Tag
  open: boolean
  onClose: () => void
  onSubmit: (values: TagFormValues) => void
  isSaving?: boolean
}>()
</script>

<template>
  <Dialog :open="props.open" @update:open="val => !val && props.onClose()">
    <DialogContent>
      <DialogTitle>Edit Tag</DialogTitle>
      <TagForm
        :tag="tag"
        :onSubmit="props.onSubmit"
        :isLoading="props.isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

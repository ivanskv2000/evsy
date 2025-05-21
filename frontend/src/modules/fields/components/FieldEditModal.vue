<script setup lang="ts">
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogHeader,
  DialogDescription,
} from '@/shared/ui/dialog'
import type { Field } from '@/modules/fields/types'
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'

defineProps<{
  description?: string
  field: Field
  open: boolean
  onClose: () => void
  onSubmit: (values: FieldFormValues) => void
  isSaving?: boolean
}>()
</script>

<template>
  <Dialog :open="open" @update:open="onClose">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Edit Field</DialogTitle>
        <DialogDescription>
          {{ description }}
        </DialogDescription>
      </DialogHeader>
      <FieldForm
        v-if="field"
        :field="field"
        :onSubmit="onSubmit"
        :isLoading="isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

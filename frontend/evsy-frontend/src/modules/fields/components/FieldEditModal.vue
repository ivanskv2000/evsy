<script setup lang="ts">
import type { Field } from '@/modules/fields/types'
import { Dialog, DialogContent, DialogTitle, DialogDescription } from '@/shared/ui/dialog'
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'

const props = defineProps<{
  description?: string
  field: Field
  open: boolean
  onClose: () => void
  onSubmit: (values: FieldFormValues) => void
  isSaving?: boolean
}>()
</script>

<template>
  <Dialog :open="props.open" @update:open="val => !val && props.onClose()">
    <DialogContent>
      <DialogTitle>Edit Field</DialogTitle>
      <DialogDescription>
        {{ description }}
      </DialogDescription>
      <FieldForm
        :field="field"
        :onSubmit="props.onSubmit"
        :isLoading="props.isSaving"
        button-text="Save"
      />
    </DialogContent>
  </Dialog>
</template>

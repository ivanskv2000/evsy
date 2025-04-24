<script setup lang="ts">
import type { Field } from '@/modules/fields/types'
import { Dialog, DialogContent, DialogTitle } from '@/shared/components/ui/dialog'
import { fieldApi } from '@/modules/fields/api'
import { useSuccessToast } from '@/shared/utils/toast'
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'

const { isLoading, run } = useAsyncTask()
const props = defineProps<{ field: Field }>()
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'updated', field: Field): void
}>()

const { showSuccessToast } = useSuccessToast()

const onSubmit = (values: FieldFormValues) => {
  run(
    () => fieldApi.update(props.field.id, values),
    updated => {
      showSuccessToast('Field updated successfully!')
      emit('updated', updated)
      emit('close')
    }
  )
}
</script>

<template>
  <Dialog :open="true" @update:open="val => !val && emit('close')">
    <DialogContent>
      <DialogTitle>Edit Field</DialogTitle>
      <FieldForm button-text="Save" :field="field" :onSubmit="onSubmit" :isLoading="isLoading" />
    </DialogContent>
  </Dialog>
</template>

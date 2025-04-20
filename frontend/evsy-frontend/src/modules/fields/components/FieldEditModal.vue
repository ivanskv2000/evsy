<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Field } from '@/modules/fields/types'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from '@/shared/components/ui/dialog'
import { Input } from '@/shared/components/ui/input'
import { Button } from '@/shared/components/ui/button'
import { fieldApi } from '@/modules/fields/api'
import { useApiErrorToast, useSuccessToast } from '@/shared/utils/toast'
import FieldForm from '@/modules/fields/components/FieldForm.vue'

const props = defineProps<{ field: Field }>()
const emit = defineEmits<{
    (e: "close"): void
    (e: "updated", field: Field): void
}>()

const isLoading = ref(false)

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()

const onSubmit = async (values) => {
    isLoading.value = true
    try {
        const updated = await fieldApi.update(props.field.id, values)
        showSuccessToast("Field updated successfully!")
        emit("updated", updated)
        emit("close")
    } catch (err) {
        showApiErrorToast(err)
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <Dialog :open="true" @update:open="(val) => !val && emit('close')">
      <DialogContent>
        <DialogTitle>Edit Field</DialogTitle>
          <FieldForm button-text="Save" :field="field" :onSubmit="onSubmit" />
      </DialogContent>
    </Dialog>
  </template>
  
<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Field } from '@/types'
import { Dialog, DialogContent, DialogTitle, DialogFooter } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { fieldApi } from '@/lib/fields'
import { useApiErrorToast } from '@/lib/useApiErrorToast'
import { useSuccessToast } from '@/lib/useSuccessToast'

const props = defineProps<{ field: Field }>()
const emit = defineEmits<{
    (e: "close"): void
    (e: "updated", field: Field): void
}>()

const name = ref(props.field.name)
const description = ref(props.field.description ?? '')
const fieldType = ref(props.field.field_type)

const isLoading = ref(false)

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()

const handleSubmit = async () => {
    isLoading.value = true
    try {
        const updated = await fieldApi.update(props.field.id, {
            name: name.value,
            description: description.value,
            field_type: fieldType.value,
        })
        showSuccessToast("Field updated successfully!")
        emit("updated", updated)
        emit("close")
    } catch (err) {
        showApiErrorToast(err)
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <Dialog :open="true" @update:open="(val) => !val && emit('close')">
      <DialogContent>
        <DialogTitle>Edit Field</DialogTitle>
  
        <div class="grid gap-4 py-4">
          <Input v-model="name" placeholder="Name" />
          <Input v-model="description" placeholder="Description" />
          <Input v-model="fieldType" placeholder="Type (e.g. string, number)" />
        </div>
  
        <DialogFooter>
          <Button variant="secondary" @click="emit('close')">Cancel</Button>
          <Button @click="handleSubmit">Save</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </template>
  
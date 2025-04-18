<script setup lang="ts">
import type { Field } from '@/types'
import { Button } from '@/components/ui/button'
import { ref } from 'vue'
import DeleteModal from '@/components/modals/DeleteModal.vue'
import FieldEditModal from '@/components/modals/FieldEditModal.vue'
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { useApiErrorToast } from '@/lib/useApiErrorToast'
import { useSuccessToast } from '@/lib/useSuccessToast'
import { useRouter } from 'vue-router'
import { fieldApi } from '@/lib/fields'

const router = useRouter()
const isLoading = ref(false)

const props = defineProps<{
  field: Field
}>()

const emit = defineEmits<{
  (e: "updated", field: Field): void
}>()

const handleUpdate = (updatedField: Field) => {
  emit("updated", updatedField)
}

const handleDelete = async () => {
    isLoading.value = true
    try {
        await fieldApi.delete(props.field.id)
        showSuccessToast("Field deleted successfully!")
        router.push('/fields')
    } catch (err) {
        console.log(err)
        showApiErrorToast(err)
    } finally {
        isLoading.value = false
    }
}

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()


</script>

<template>
  <Card>
    <CardHeader>
            <CardTitle>{{ field.name }}</CardTitle>
            <CardDescription>{{ field.field_type }}</CardDescription>
        </CardHeader>
    <CardContent>

        <div v-if="field.description">
            <p class="text-muted-foreground text-sm mb-1">Description</p>
            <p>{{ field.description }}</p>
        </div>

    </CardContent>

    <CardFooter class="flex justify-left space-x-3 px-6 pb-6">
        <Button variant="secondary" @click="showEditModal = true">Edit</Button>
        <Button variant="destructive" @click="showDeleteModal = true">Delete</Button>
    </CardFooter>

    <FieldEditModal 
        v-if="showEditModal"
        :field="field"
        @close="showEditModal = false"
        @updated="handleUpdate"
    />
    <DeleteModal 
        :open="showDeleteModal"
        :onClose="() => (showDeleteModal = false)"
        :onConfirm="handleDelete"
        description="Once deleted, this field will be unlinked from any events it's part of."
    />
  </Card>
</template>

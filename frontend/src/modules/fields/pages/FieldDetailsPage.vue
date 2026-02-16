<script setup lang="ts">
import { defineAsyncComponent, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import FieldDetailsCard from '@/modules/fields/components/FieldDetailsCard.vue'
import { fieldApi } from '@/modules/fields/api'
import Header from '@/shared/components/layout/PageHeader.vue'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import DetailsCardSkeleton from '@/shared/components/skeletons/DetailsCardSkeleton.vue'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const FieldEditModal = defineAsyncComponent(
  () => import('@/modules/fields/components/FieldEditModal.vue')
)

const route = useRoute()
const router = useRouter()
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const queryClient = useQueryClient()
const { showDeleted, showUpdated } = useEnhancedToast()
const fieldId = Number(route.params.id)

const { data: field, isLoading } = useQuery({
  queryKey: ['fields', fieldId],
  queryFn: () => fieldApi.getById(fieldId, { with_event_count: true })
})

const { mutate: deleteField, isPending: isDeleting } = useMutation({
  mutationFn: () => fieldApi.delete(fieldId),
  onSuccess: () => {
    showDeleted('Field')
    queryClient.invalidateQueries({ queryKey: ['fields'] })
    router.push('/fields')
  }
})

const { mutate: updateField, isPending: isSaving } = useMutation({
  mutationFn: (values: FieldFormValues) => fieldApi.update(fieldId, values),
  onSuccess: () => {
    showUpdated('Field')
    queryClient.invalidateQueries({ queryKey: ['fields', fieldId] })
    queryClient.invalidateQueries({ queryKey: ['fields'] })
    showEditModal.value = false
  }
})

const handleDelete = () => {
  deleteField()
}

const handleUpdate = (values: FieldFormValues) => {
  updateField(values)
}
</script>

<template>
  <div>
    <Header title="Field details" backLink fallbackBackLink="/fields" />

    <DetailsCardSkeleton v-if="isLoading || !field" />

    <FieldDetailsCard
      v-else
      :field="field"
      :isLoading="isLoading"
      @edit-clicked="showEditModal = true"
      @delete-clicked="showDeleteModal = true"
    />

    <FieldEditModal
      v-if="field"
      :open="showEditModal"
      :field="field"
      :onClose="() => (showEditModal = false)"
      :onSubmit="handleUpdate"
      :isSaving="isSaving"
    />

    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="handleDelete"
      :isDeleting="isDeleting"
      description="Once deleted, this field will be unlinked from any events it's part of."
    />
  </div>
</template>

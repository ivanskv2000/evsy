<script setup lang="ts">
import { ref, defineAsyncComponent } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import FieldsDataTable from '@/modules/fields/components/FieldsDataTable.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { getFieldColumns } from '@/modules/fields/components/fieldColumns'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import { useUrlFilters, fieldsFiltersConfig } from '@/shared/composables/useUrlFilters'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const FieldEditModal = defineAsyncComponent(
  () => import('@/modules/fields/components/FieldEditModal.vue')
)

const queryClient = useQueryClient()
const { showUpdated, showDeleted } = useEnhancedToast()

const selectedFieldId = ref<number | null>(null)
const editedField = ref<Field | null>(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const urlFilters = useUrlFilters(fieldsFiltersConfig)

const { data: fields, isLoading } = useQuery({
  queryKey: ['fields'],
  queryFn: () => fieldApi.getAll(),
})

const { mutate: deleteField, isPending: isDeleting } = useMutation({
  mutationFn: (id: number) => fieldApi.delete(id),
  onSuccess: () => {
    showDeleted('Field')
    queryClient.invalidateQueries({ queryKey: ['fields'] })
  }
})

const { mutate: updateField, isPending: isSaving } = useMutation({
  mutationFn: ({ id, values }: { id: number; values: FieldFormValues }) =>
    fieldApi.update(id, values),
  onSuccess: () => {
    showUpdated('Field')
    queryClient.invalidateQueries({ queryKey: ['fields'] })
  }
})

const handleDelete = () => {
  if (!selectedFieldId.value) return
  deleteField(selectedFieldId.value)
  showDeleteModal.value = false
}

const handleUpdate = (values: FieldFormValues) => {
  if (!editedField.value) return
  updateField({ id: editedField.value.id, values })
  showEditModal.value = false
}

const selectEditField = (field: Field) => {
  editedField.value = field
  showEditModal.value = true
}

const selectDeleteField = (field: Field) => {
  selectedFieldId.value = field.id
  showDeleteModal.value = true
}

const columns = getFieldColumns(selectEditField, selectDeleteField)
</script>

<template>
  <div>
    <Header title="Fields" />
    <div class="container mx-auto">
      <FieldsDataTable
        :columns="columns"
        :data="fields ?? []"
        :isLoading="isLoading"
        :url-filters="urlFilters"
      />
    </div>

    <!-- Modals -->
    <FieldEditModal
      v-if="editedField"
      :open="showEditModal"
      :field="editedField"
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

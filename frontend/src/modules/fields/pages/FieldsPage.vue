<script setup lang="ts">
import { ref, onMounted, defineAsyncComponent } from 'vue'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import FieldsDataTable from '@/modules/fields/components/FieldsDataTable.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { getFieldColumns } from '@/modules/fields/components/fieldColumns'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import { useUrlFilters, fieldsFiltersConfig } from '@/shared/composables/useUrlFilters'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const FieldEditModal = defineAsyncComponent(
  () => import('@/modules/fields/components/FieldEditModal.vue')
)

const { run, isLoading } = useAsyncTask()
const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()
const { showUpdated, showDeleted } = useEnhancedToast()

const fields = ref<Field[]>([])

const selectedFieldId = ref<number | null>(null)
const editedField = ref<Field | null>(null)

const urlFilters = useUrlFilters(fieldsFiltersConfig)

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const updateRow = (updated: Field) => {
  const index = fields.value.findIndex(f => f.id === updated.id)
  if (index !== -1) {
    fields.value = fields.value.map(f => (f.id === updated.id ? updated : f))
  }
}
const deleteRow = (id: number) => {
  fields.value = fields.value.filter(f => f.id !== id)
}

const handleDelete = () => {
  if (!selectedFieldId.value) return

  runDeleteTask(async () => {
    await fieldApi.delete(selectedFieldId.value!)
    showDeleted('Field')
    deleteRow(selectedFieldId.value!)
    selectedFieldId.value = null
    showDeleteModal.value = false
  })
}

const handleUpdate = (values: FieldFormValues) => {
  runUpdateTask(
    () => fieldApi.update(editedField.value!.id, values),
    updated => {
      showUpdated('Field')
      updateRow(updated)
      editedField.value = null
      showEditModal.value = false
    }
  )
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

onMounted(() => {
  run(
    () => fieldApi.getAll(),
    data => {
      fields.value = data
    }
  )
})
</script>

<template>
  <div>
    <Header title="Fields" />
    <div class="container mx-auto">
      <FieldsDataTable
        :columns="columns"
        :data="fields"
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

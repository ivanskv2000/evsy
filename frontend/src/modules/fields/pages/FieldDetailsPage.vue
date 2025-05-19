<script setup lang="ts">
import { defineAsyncComponent, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { Field } from '@/modules/fields/types'
import FieldDetailsCard from '@/modules/fields/components/FieldDetailsCard.vue'
import { fieldApi } from '@/modules/fields/api'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import DetailsCardSkeleton from '@/shared/components/skeletons/DetailsCardSkeleton.vue'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const FieldEditModal = defineAsyncComponent(
  () => import('@/modules/fields/components/FieldEditModal.vue')
)

const route = useRoute()
const router = useRouter()
const field = ref<Field | null>(null)
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { run, isLoading } = useAsyncTask()
const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()

const { showDeleted, showUpdated } = useEnhancedToast()

const handleDelete = () => {
  runDeleteTask(async () => {
    await fieldApi.delete(field.value!.id)
    showDeleted('Field')
    router.push('/fields')
  })
}

const handleUpdate = (values: FieldFormValues) => {
  runUpdateTask(
    () => fieldApi.update(field.value!.id, values),
    updated => {
      showUpdated('Field')
      field.value = updated
      showEditModal.value = false
    }
  )
}

onMounted(() => {
  const id = Number(route.params.id)
  run(
    () => fieldApi.getById(id, { with_event_count: true }),
    result => {
      if (result) field.value = result
    }
  )
})
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

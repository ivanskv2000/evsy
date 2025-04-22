<script setup lang="ts">
import TagItem from '../components/TagItem.vue'
import { tagApi } from '@/modules/tags/api'
import type { Tag } from '@/modules/tags/types'
import { ref, onMounted } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import DeleteModal from '@/shared/components/data/DeleteModal.vue'
import TagEditModal from '@/modules/tags/components/TagEditModal.vue'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import Header from '@/shared/components/layout/Header.vue'

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
const { showInfoToast } = useInfoToast()

const tags = ref<Tag[]>([])
const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const selectedTagId = ref<string | null>(null)
const editedTag = ref<Tag | null>(null)

const handleUpdate = (updatedTag: Tag) => {
  emit('updated', updatedTag)
}

const handleDelete = () => {
  if (!selectedTagId.value) return

  runDeleteTask(async () => {
    await tagApi.delete(selectedTagId.value!)
    showSuccessToast('Tag deleted successfully!')
    showDeleteModal.value = false

    tags.value = tags.value.filter(tag => tag.id !== selectedTagId.value)
    selectedTagId.value = null
  })
}

const handleEditSubmit = (values: TagFormValues) => {
  runUpdateTask(
    () => tagApi.update(editedTag.value!.id, values),
    updated => {
      showSuccessToast('Tag updated successfully!')
      tags.value = tags.value.map(tag => tag.id === updated.id ? updated : tag)
      showEditModal.value = false
    }
  )
}



const { run, isLoading } = useAsyncTask()

onMounted(() => {
  run(
    () => tagApi.getAll(),
    data => {
      tags.value = data
    }
  )
})
</script>

<template>
  <div>
    <Header title="Tags" />
    <div class="container mx-auto">
      <FieldsDataTable :columns="columns" :data="fields" />
    </div>
    <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2">
      <TagItem
        v-for="tag in tags"
        :key="tag.id"
        :tag="tag"
        @updateMe="(id) => { showEditModal = true; editedTag = tag; }"
        @deleteMe="(id) => { showDeleteModal = true; selectedTagId = id; }"
        />
    </div>
  </div>

  <TagEditModal
    v-if="editedTag"
    :open="showEditModal"
    :tag="editedTag"
    :onClose="() => (showEditModal = false)"
    :onSubmit="handleEditSubmit"
    :isSaving="isSaving"
  />
  <DeleteModal 
    :open="showDeleteModal" 
    :onClose="() => (showDeleteModal = false)" 
    :onConfirm="handleDelete"
    :isDeleting="isDeleting" 
    description="Once deleted, this tag will be unlinked from any events it's part of." 
  />
</template>

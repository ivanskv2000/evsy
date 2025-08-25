<script setup lang="ts">
import TagsDataGrid from '../components/TagsDataGrid.vue'
import { tagApi } from '@/modules/tags/api'
import type { Tag } from '@/modules/tags/types'
import { ref, onMounted, defineAsyncComponent, computed } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useUrlFilters, tagsFiltersConfig } from '@/shared/composables/useUrlFilters'
import { filterTags } from '@/shared/utils/tableFilters'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const TagEditModal = defineAsyncComponent(
  () => import('@/modules/tags/components/TagEditModal.vue')
)

const { showUpdated, showDeleted } = useEnhancedToast()

const tags = ref<Tag[]>([])
const { run, isLoading } = useAsyncTask()
const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const selectedTagId = ref<string | null>(null)
const editedTag = ref<Tag | null>(null)

// URL filters with search synchronization
const urlFilters = useUrlFilters(tagsFiltersConfig)

// Filter tags based on URL search
const filteredTags = computed(() => {
  return filterTags(tags.value, urlFilters.filters.search)
})

const handleDelete = () => {
  if (!selectedTagId.value) return

  runDeleteTask(async () => {
    await tagApi.delete(selectedTagId.value!)
    showDeleted('Tag')
    tags.value = tags.value.filter(tag => tag.id !== selectedTagId.value)
    selectedTagId.value = null
    showDeleteModal.value = false
  })
}

const handleUpdate = (values: TagFormValues) => {
  runUpdateTask(
    () => tagApi.update(editedTag.value!.id, values),
    updated => {
      showUpdated('Tag')
      tags.value = tags.value.map(tag => (tag.id === updated.id ? updated : tag))
      showEditModal.value = false
    }
  )
}

// Handlers for TagsDataGrid
const selectEditTag = (tag: Tag) => {
  editedTag.value = tag
  showEditModal.value = true
}

const selectDeleteTag = (tag: Tag) => {
  selectedTagId.value = tag.id
  showDeleteModal.value = true
}

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
  <div class="container mx-auto">
    <Header title="Tags" />

    <TagsDataGrid
      :filtered-data="filteredTags"
      :isLoading="isLoading"
      :url-filters="urlFilters"
      :onEdit="selectEditTag"
      :onDelete="selectDeleteTag"
    />

    <!-- Modals -->
    <TagEditModal
      v-if="editedTag"
      :open="showEditModal"
      :tag="editedTag"
      :onClose="() => (showEditModal = false)"
      :onSubmit="handleUpdate"
      :isSaving="isSaving"
    />
    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="handleDelete"
      :isDeleting="isDeleting"
      description="Once deleted, this tag will be unlinked from any events it's part of."
    />
  </div>
</template>

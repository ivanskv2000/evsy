<script setup lang="ts">
import TagsDataGrid from '../components/TagsDataGrid.vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { tagApi } from '@/modules/tags/api'
import type { Tag } from '@/modules/tags/types'
import { ref, defineAsyncComponent, computed } from 'vue'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import Header from '@/shared/components/layout/PageHeader.vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useUrlFilters, tagsFiltersConfig } from '@/shared/composables/useUrlFilters'
import { filterTags } from '@/shared/utils/tableFilters'

const DeleteModal = defineAsyncComponent(() => import('@/shared/components/modals/DeleteModal.vue'))
const TagEditModal = defineAsyncComponent(
  () => import('@/modules/tags/components/TagEditModal.vue')
)

const queryClient = useQueryClient()
const { showUpdated, showDeleted } = useEnhancedToast()

const selectedTagId = ref<string | null>(null)
const editedTag = ref<Tag | null>(null)

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const urlFilters = useUrlFilters(tagsFiltersConfig)

const { data: tags, isLoading } = useQuery({
  queryKey: ['tags'],
  queryFn: () => tagApi.getAll(),
})

const { mutate: deleteTag, isPending: isDeleting } = useMutation({
  mutationFn: (id: string) => tagApi.delete(id),
  onSuccess: () => {
    showDeleted('Tag')
    queryClient.invalidateQueries({ queryKey: ['tags'] })
  }
})

const { mutate: updateTag, isPending: isSaving } = useMutation({
  mutationFn: ({ id, values }: { id: string; values: TagFormValues }) =>
    tagApi.update(id, values),
  onSuccess: () => {
    showUpdated('Tag')
    queryClient.invalidateQueries({ queryKey: ['tags'] })
  }
})

const handleDelete = () => {
  if (!selectedTagId.value) return
  deleteTag(selectedTagId.value)
  showDeleteModal.value = false
}

const handleUpdate = (values: TagFormValues) => {
  if (!editedTag.value) return
  updateTag({ id: editedTag.value.id, values })
  showEditModal.value = false
}

const selectEditTag = (tag: Tag) => {
  editedTag.value = tag
  showEditModal.value = true
}

const selectDeleteTag = (tag: Tag) => {
  selectedTagId.value = tag.id
  showDeleteModal.value = true
}

const filteredTags = computed(() => {
  return filterTags(tags.value ?? [], urlFilters.filters.search)
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

<script setup lang="ts">
import TagItem from '../components/TagItem.vue'
import { tagApi } from '@/modules/tags/api'
import type { Tag } from '@/modules/tags/types'
import { ref, onMounted, computed } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import TagEditModal from '@/modules/tags/components/TagEditModal.vue'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import Header from '@/shared/components/layout/Header.vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

const { showUpdated, showDeleted } = useEnhancedToast()

const tags = ref<Tag[]>([])
const searchQuery = ref('')
const { run: runDeleteTask, isLoading: isDeleting } = useAsyncTask()
const { run: runUpdateTask, isLoading: isSaving } = useAsyncTask()

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const selectedTagId = ref<string | null>(null)
const editedTag = ref<Tag | null>(null)

const filteredTags = computed(() => {
  if (!searchQuery.value) return tags.value
  const query = searchQuery.value.toLowerCase()
  return tags.value.filter(tag => 
    tag.id.toLowerCase().includes(query) || 
    (tag.description?.toLowerCase().includes(query) ?? false)
  )
})

const handleDelete = () => {
  if (!selectedTagId.value) return

  runDeleteTask(async () => {
    await tagApi.delete(selectedTagId.value!)
    showDeleted('Tag')
    showDeleteModal.value = false

    tags.value = tags.value.filter(tag => tag.id !== selectedTagId.value)
    selectedTagId.value = null
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

const { run } = useAsyncTask()

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
    
    <!-- Toolbar -->
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div class="flex-1">
        <Input
          v-model="searchQuery"
          placeholder="Search tags..."
          class="max-w-xs"
        >
        </Input>
      </div>
      <Button as-child>
        <RouterLink to="/tags/new">
          <Icon icon="radix-icons:plus" class="mr-2 h-4 w-4" />
          Add Tag
        </RouterLink>
      </Button>
    </div>

    <!-- Tags Grid -->
    <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2">
      <TagItem
        v-for="tag in filteredTags"
        :key="tag.id"
        :tag="tag"
        @updateMe="
          () => {
            showEditModal = true
            editedTag = tag
          }
        "
        @deleteMe="
          id => {
            showDeleteModal = true
            selectedTagId = id
          }
        "
      />
    </div>

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

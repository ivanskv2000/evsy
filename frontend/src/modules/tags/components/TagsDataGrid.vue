<script setup lang="ts">
import { ref, watch } from 'vue'
import TagItem from './TagItem.vue'
import type { Tag } from '@/modules/tags/types'
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'
import ItemSkeleton from '@/shared/components/skeletons/ItemSkeleton.vue'
import { RouterLink } from 'vue-router'
import { useDebounceFn } from '@vueuse/core'

interface TagsDataGridProps {
  filteredData: Tag[]
  isLoading: boolean
  searchValue: string
  onEdit: (tag: Tag) => void
  onDelete: (tag: Tag) => void
}

const props = defineProps<TagsDataGridProps>()
const emit = defineEmits<{
  'update:searchValue': [value: string]
}>()

const localSearchValue = ref(props.searchValue)

const debouncedEmit = useDebounceFn((value: string) => {
  emit('update:searchValue', value)
}, 300)

watch(localSearchValue, newValue => {
  debouncedEmit(newValue)
})

watch(
  () => props.searchValue,
  newValue => {
    if (newValue !== localSearchValue.value) {
      localSearchValue.value = newValue
    }
  }
)

const handleSearchKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    localSearchValue.value = ''
  }
}
</script>

<template>
  <div>
    <!-- Toolbar -->
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div class="flex-1">
        <Input
          v-model="localSearchValue"
          autocomplete="off"
          placeholder="Search tags..."
          class="max-w-xs"
          @keydown="handleSearchKeydown"
        />
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
      <template v-if="isLoading">
        <ItemSkeleton v-for="n in 4" :key="n" />
      </template>

      <template v-else-if="filteredData.length > 0">
        <TagItem
          v-for="tag in filteredData"
          :key="tag.id"
          :tag="tag"
          @updateMe="() => onEdit(tag)"
          @deleteMe="() => onDelete(tag)"
        />
      </template>

      <template v-else>
        <div class="col-span-full w-full rounded-lg border p-4 text-center text-sm">
          <div>No results.</div>
        </div>
      </template>
    </div>
  </div>
</template>

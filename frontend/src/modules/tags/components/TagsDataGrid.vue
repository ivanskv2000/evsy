<script setup lang="ts">
import TagItem from './TagItem.vue'
import type { Tag } from '@/modules/tags/types'
import type { UrlFiltersReturn, TagsUrlFilters } from '@/shared/types/urlFilters'
import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'
import ItemSkeleton from '@/shared/components/skeletons/ItemSkeleton.vue'
import { RouterLink } from 'vue-router'
interface TagsDataGridProps {
  filteredData: Tag[]
  isLoading: boolean
  urlFilters: UrlFiltersReturn<TagsUrlFilters>
  onEdit: (tag: Tag) => void
  onDelete: (tag: Tag) => void
}

const props = defineProps<TagsDataGridProps>()

const handleSearchKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    props.urlFilters.clearFilters()
  }
}
</script>

<template>
  <div>
    <!-- Toolbar -->
    <div class="mb-6 flex flex-wrap items-center justify-between gap-4">
      <div class="flex-1">
        <Input
          :model-value="urlFilters.filters.search"
          @update:model-value="(value: string | number) => urlFilters.updateSearch?.(String(value))"
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
        <div class="col-span-full flex items-center justify-center py-6">
          <div class="text-center">
            <div class="text-sm">No results.</div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

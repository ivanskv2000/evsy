<script setup lang="ts">
import TagItem from '../components/TagItem.vue'
import { tagApi } from '@/modules/tags/api'
import type { Tag } from '@/modules/tags/types'
import { ref, onMounted } from 'vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const tags = ref<Tag[]>([])
const { run, isLoading } = useAsyncTask()

onMounted(() => {
  run(() => tagApi.getAll(), (data) => {
    tags.value = data
  })
})
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <h1 class="flex-1 text-center text-2xl font-bold">Tags</h1>
    </div>

    <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2">
      <TagItem v-for="tag in tags" :key="tag.id" :tag="tag" />
    </div>
  </div>
</template>

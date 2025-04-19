<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import TagItem from '../components/TagItem.vue'
import { tagApi } from '@/modules/tags/api'
import type { Tag } from '@/modules/tags/types'
import { useApiErrorToast } from '@/shared/utils/toast'
import { ref, onMounted } from 'vue'

const tags = ref<Field[]>([])
const isLoading = ref(true)
const { showApiErrorToast } = useApiErrorToast()

onMounted(async () => {
  try {
    tags.value = await tagApi.getAll()
  } catch (err) {
    showApiErrorToast(err)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-center flex-1">Tags</h1>
    </div>


    <div class="grid gap-4 sm:grid-cols-1 md:grid-cols-2">
      <TagItem v-for="tag in tags" :key="tag.id" :tag="tag" />
    </div>
  </div>
</template> 
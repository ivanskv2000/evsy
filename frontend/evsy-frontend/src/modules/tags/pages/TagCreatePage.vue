<script setup lang="ts">
import TagForm from '@/modules/tags/components/TagForm.vue'
import { useRouter } from 'vue-router'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { tagApi } from '@/modules/tags/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import Header from '@/shared/components/layout/Header.vue'
import {
  Card,
  CardContent
} from '@/shared/ui/card'

const { isLoading, run } = useAsyncTask()
const { showCreated } = useEnhancedToast()
const router = useRouter()

const onSubmit = (values: TagFormValues) => {
  run(
    () => tagApi.create(values),
    () => {
      router.push('/tags')
      showCreated('Tag')
    }
  )
}
</script>

<template>
  <div>
    <Header title="Create new tag" backLink fallbackBackLink="/tags" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <TagForm 
          :onSubmit="onSubmit"
          :isLoading="isLoading"
          button-text="Create"
        />
      </CardContent>
    </Card>
  </div>
</template> 
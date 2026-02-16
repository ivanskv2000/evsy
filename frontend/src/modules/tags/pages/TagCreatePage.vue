<script setup lang="ts">
import TagForm from '@/modules/tags/components/TagForm.vue'
import { useRouter } from 'vue-router'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { tagApi } from '@/modules/tags/api'
import type { TagFormValues } from '@/modules/tags/validation/tagSchema'
import Header from '@/shared/components/layout/PageHeader.vue'
import { Card, CardContent } from '@/shared/ui/card'

const { showCreated } = useEnhancedToast()
const router = useRouter()
const queryClient = useQueryClient()

const { mutate: createTag, isPending: isLoading } = useMutation({
  mutationFn: (values: TagFormValues) => tagApi.create(values),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['tags'] })
    router.push('/tags')
    showCreated('Tag')
  }
})

const onSubmit = (values: TagFormValues) => {
  createTag(values)
}
</script>

<template>
  <div>
    <Header title="Create new tag" backLink fallbackBackLink="/tags" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <TagForm :onSubmit="onSubmit" :isLoading="isLoading" button-text="Create" />
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import { useRouter } from 'vue-router'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { fieldApi } from '@/modules/fields/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import Header from '@/shared/components/layout/Header.vue'
import {
  Card,
  CardContent
} from '@/shared/components/ui/card'

const { isLoading, run } = useAsyncTask()
const { showCreated } = useEnhancedToast()
const router = useRouter()

const onSubmit = (values: FieldFormValues) => {
  run(
    () => fieldApi.create(values),
    created => {
      router.push(`/fields/${created.id}`)
      showCreated('Field')
    }
  )
}
</script>

<template>
  <div>
    <Header title="Create new field" backLink fallbackBackLink="/fields" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <FieldForm :onSubmit="onSubmit" :isLoading="isLoading" />
      </CardContent>
    </Card>
  </div>
</template>

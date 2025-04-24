<script setup lang="ts">
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import { Button } from '@/shared/components/ui/button'
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'
import { useSuccessToast } from '@/shared/utils/toast'
import { ref } from 'vue'
import { fieldApi } from '@/modules/fields/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import Header from '@/shared/components/layout/Header.vue'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/shared/components/ui/card'

const { isLoading, run } = useAsyncTask()
const { showSuccessToast } = useSuccessToast()
const router = useRouter()

const onSubmit = (values: FieldFormValues) => {
  run(
    () => fieldApi.create(values),
    created => {
      router.push(`/fields/${created.id}`)
      showSuccessToast('Field created successfully!')
    }
  )
}
</script>

<template>
  <div>
    <Header title="Create new field" backLink fallbackBackLink="/fields" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <FieldForm :onSubmit="onSubmit" />
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import { useRouter } from 'vue-router'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import Header from '@/shared/components/layout/PageHeader.vue'
import { Card, CardContent } from '@/shared/ui/card'

const { showCreated } = useEnhancedToast()
const router = useRouter()
const queryClient = useQueryClient()

const { mutate: createField, isPending: isLoading } = useMutation({
  mutationFn: (values: FieldFormValues) => fieldApi.create(values),
  onSuccess: (createdField: Field) => {
    queryClient.invalidateQueries({ queryKey: ['fields'] })
    router.push(`/fields/${createdField.id}`)
    showCreated('Field')
  }
})

const onSubmit = (values: FieldFormValues) => {
  createField(values)
}
</script>

<template>
  <div>
    <Header title="Create new field" backLink fallbackBackLink="/fields" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <FieldForm :onSubmit="onSubmit" :isLoading="isLoading" button-text="Create" />
      </CardContent>
    </Card>
  </div>
</template>

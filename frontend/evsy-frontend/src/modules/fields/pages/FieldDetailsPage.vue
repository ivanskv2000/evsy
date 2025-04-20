<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import type { Field } from '@/modules/fields/types'
import FieldDetailsCard from '@/modules/fields/components/FieldDetailsCard.vue'
import { useApiErrorToast } from '@/shared/utils/toast'
import { fieldApi } from '@/modules/fields/api'
import Header from '@/shared/components/layout/Header.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
const { showApiErrorToast } = useApiErrorToast()
const route = useRoute()
const field = ref<Field | null>(null)
const { run, isLoading } = useAsyncTask()

const handleUpdate = (updatedField: Field) => {
  field.value = updatedField
}

onMounted(() => {
  const id = Number(route.params.id)
  run(() => fieldApi.getById(id), (result) => {
    if (result) field.value = result
  })
})
</script>

<template>
  <div>
    <Header title="Field details" backLink="/fields" />
    <FieldDetailsCard v-if="field" :field="field!" @updated="handleUpdate" />
  </div>
</template>

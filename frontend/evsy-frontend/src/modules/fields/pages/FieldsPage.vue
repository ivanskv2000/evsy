<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import FieldsDataTable from '@/modules/fields/components/FieldsDataTable.vue'
import Header from '@/shared/components/layout/Header.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const fields = ref<Field[]>([])
import { getFieldColumns } from '@/modules/fields/components/fieldColumns'
const updateRow = (updated: Field) => {
  const index = fields.value.findIndex((f) => f.id === updated.id)
  if (index !== -1) {
    fields.value = fields.value.map((f) => 
      f.id === updated.id ? updated : f
    )
  }
}
const deleteRow = (id: number) => {
  fields.value = fields.value.filter((f) => f.id !== id)
}
const columns = getFieldColumns(updateRow, deleteRow)
const { isLoading, run } = useAsyncTask()

onMounted(() => {
  run(
    () => fieldApi.getAll(),
    data => {
      fields.value = data
    }
  )
})
</script>

<template>
  <div>
    <Header title="Fields" />
    <div class="container mx-auto">
      <FieldsDataTable :columns="columns" :data="fields" />
    </div>
  </div>
</template>

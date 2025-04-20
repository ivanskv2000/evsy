<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import { columns } from '@/modules/fields/components/columns'
import DataTable from '@/shared/components/data/DataTable.vue'
import { useApiErrorToast } from '@/shared/utils/toast'
import Header from '@/shared/components/layout/Header.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const fields = ref<Field[]>([])
const { isLoading, run } = useAsyncTask()

onMounted(() => {
  run(() => fieldApi.getAll(), (data) => {
    fields.value = data
  })
})
</script>

<template>
  <div>
    <Header title="Fields" />
    <div class="container mx-auto">
      <DataTable :columns="columns" :data="fields" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { ref, onMounted } from 'vue'
import { fieldApi } from '@/lib/fields'
import type { Field } from '@/types'
import { columns } from '@/components/tables/fields/columns'
import DataTable from '@/components/tables/DataTable.vue'
import { useApiErrorToast } from '@/lib/useApiErrorToast'


const fields = ref<Field[]>([])
const isLoading = ref(true)
const { showApiErrorToast } = useApiErrorToast()

onMounted(async () => {
  try {
    fields.value = await fieldApi.getAll()
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
      <h1 class="text-2xl font-bold text-center flex-1">Fields</h1>
    </div>


    <div class="container mx-auto">
      <DataTable :columns="columns" :data="fields" />
    </div>
  </div>
</template> 
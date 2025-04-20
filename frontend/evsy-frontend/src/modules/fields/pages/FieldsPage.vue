<script setup lang="ts">
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/shared/components/ui/card'
import { ref, onMounted } from 'vue'
import { fieldApi } from '@/modules/fields/api'
import type { Field } from '@/modules/fields/types'
import { columns } from '@/modules/fields/components/columns'
import DataTable from '@/shared/components/data/DataTable.vue'
import { useApiErrorToast } from '@/shared/utils/toast'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/components/ui/button'

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
    <!-- Header with Back button and Title -->
    <div class="mb-6 flex items-center justify-between">
      <!-- Пустой элемент для симметрии -->
      <div class="w-[60px]"></div>

      <h1 class="flex-1 text-center text-2xl font-bold">Fields</h1>

      <Button as-child class="w-[60px]">
        <RouterLink to="/fields/new">
          <Icon icon="radix-icons:plus" class="h-4 w-4" />
        </RouterLink>
      </Button>
    </div>

    <div class="container mx-auto">
      <DataTable :columns="columns" :data="fields" />
    </div>
  </div>
</template>

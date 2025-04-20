<script setup lang="ts">
import FieldForm from '@/modules/fields/components/FieldForm.vue'
import { Button } from '@/shared/components/ui/button'
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'
import { useApiErrorToast, useSuccessToast } from '@/shared/utils/toast'
import { ref } from 'vue'
import { fieldApi } from '@/modules/fields/api'
const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
const router = useRouter()
const isLoading = ref(false)

const onSubmit = async values => {
  isLoading.value = true
  try {
    const created = await fieldApi.create(values)
    router.push(`/fields/${created.id}`)
    showSuccessToast('Field created successfully!')
  } catch (err) {
    showApiErrorToast(err)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <!-- Header with Back button and Title -->
    <div class="mb-6 flex items-center justify-between">
      <Button as-child variant="ghost" class="w-[30px]">
        <RouterLink to="/fields">
          <Icon icon="radix-icons:caret-left" class="h-4 w-4" />
        </RouterLink>
      </Button>

      <h1 class="flex-1 text-center text-2xl font-bold">Create new field</h1>

      <!-- Пустой элемент для симметрии -->
      <div class="w-[30px]"></div>
    </div>

    <FieldForm :onSubmit="onSubmit" />
  </div>
</template>

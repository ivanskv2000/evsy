<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import type { Field } from '@/modules/fields/types'
import FieldDetailsCard from '@/modules/fields/components/FieldDetailsCard.vue'
import { useApiErrorToast } from '@/shared/utils/toast'
import { fieldApi } from '@/modules/fields/api'
import { Button } from '@/shared/components/ui/button'
import { Icon } from '@iconify/vue'

const { showApiErrorToast } = useApiErrorToast()
const route = useRoute()
const field = ref<Field | null>(null)
const isLoading = ref(true)

const handleUpdate = (updatedField: Field) => {
  field.value = updatedField
}

onMounted(async () => {
  try {
    const id = route.params.id as number
    field.value = await fieldApi.getById(id)
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
        <Button as-child variant="ghost" class="w-[30px]">
            <RouterLink to="/fields">
                <Icon icon="radix-icons:caret-left" class="h-4 w-4" />
            </RouterLink>
        </Button>

      <h1 class="text-2xl font-bold text-center flex-1">Field details</h1>

      <!-- Пустой элемент для симметрии -->
      <div class="w-[30px]"></div>
    </div>


    <div v-if="isLoading">Loading...</div>
        <FieldDetailsCard v-else :field="field!" @updated="handleUpdate"/>
    </div>
</template>

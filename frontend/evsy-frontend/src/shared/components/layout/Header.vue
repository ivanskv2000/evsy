<script setup lang="ts">
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps<{
  title: string
  backLink?: boolean
  fallbackBackLink?: string
}>()

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    if (props.fallbackBackLink) {
      router.push(props.fallbackBackLink)
    }
  }
}
</script>

<template>
  <div class="mb-6 flex items-center justify-between">
    <Button v-if="backLink || false" variant="ghost" class="w-[30px]" @click="goBack">
      <Icon icon="radix-icons:caret-left" class="h-4 w-4" />
    </Button>

    <div class="mx-auto">
      <h1 class="scroll-m-20 text-2xl font-semibold tracking-tight">
        {{ title }}
      </h1>
    </div>

    <!-- Пустой элемент для симметрии -->
    <div v-if="backLink || false" class="w-[30px]"></div>
  </div>
</template>

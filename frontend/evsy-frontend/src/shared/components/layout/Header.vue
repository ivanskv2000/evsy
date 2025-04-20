<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/shared/components/ui/button'
import { Icon } from '@iconify/vue'
import { computed } from 'vue'

const props = defineProps<{
  title: string,
  backLink?: string,
}>()

const hasBackLink = computed(() => props.backLink !== undefined)
</script>

<template>
    <div class="mb-6 flex items-center justify-between">
      <Button as-child v-if="hasBackLink" variant="ghost" class="w-[30px]">
        <RouterLink :to="backLink!">
          <Icon icon="radix-icons:caret-left" class="h-4 w-4" />
        </RouterLink>
      </Button>

    <div class="mx-auto">
      <h1 class="scroll-m-20 text-2xl font-semibold tracking-tight">
        {{ title }}
        </h1>
      </div>

      <!-- Пустой элемент для симметрии -->
      <div v-if="hasBackLink" class="w-[30px]"></div>
    </div>
</template>
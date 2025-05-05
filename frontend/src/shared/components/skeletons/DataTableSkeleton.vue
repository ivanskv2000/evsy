<script setup lang="ts">
import { Skeleton } from '@/shared/ui/skeleton'

const props = withDefaults(
  defineProps<{
    rows?: number
    columns?: number
  }>(),
  {
    rows: 5,
    columns: 4,
  }
)
</script>

<template>
  <div class="rounded-md border">
    <div class="divide-y">
      <!-- Fake headers -->
      <div class="flex items-center p-4">
        <Skeleton
          v-for="i in props.columns"
          :key="'header-' + i"
          class="mr-4 h-4 flex-1 last:mr-0"
        />
      </div>

      <!-- Fake rows -->
      <div
        v-for="row in props.rows"
        :key="'row-' + row"
        class="flex animate-pulse items-center space-x-4 p-4"
      >
        <Skeleton v-for="i in props.columns" :key="`cell-${row}-${i}`" class="h-4 flex-1" />
      </div>
    </div>
  </div>
</template>

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
        <Skeleton v-for="i in props.columns" :key="'header-' + i" class="h-4 flex-1 mr-4 last:mr-0" />
      </div>

      <!-- Fake rows -->
      <div
        v-for="row in props.rows"
        :key="'row-' + row"
        class="flex items-center p-4 animate-pulse space-x-4"
      >
        <Skeleton
          v-for="i in props.columns"
          :key="`cell-${row}-${i}`"
          class="h-4 flex-1"
        />
      </div>
    </div>
  </div>
</template>
<template>
  <div class="flex items-start justify-between gap-4 rounded-lg border p-4">
    <div class="flex-1 space-y-2">
      <Skeleton class="h-5 w-28 rounded" />
      <Skeleton class="h-4 w-40 rounded" />
    </div>
    <div class="flex gap-2">
      <Skeleton class="h-8 w-8 rounded" />
      <Skeleton class="h-8 w-8 rounded" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Skeleton } from '@/shared/ui/skeleton'
</script>

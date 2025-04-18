<script setup lang="ts">
import { Skeleton } from '@/components/ui/skeleton'
</script>

<template>
    <div class="space-y-4">
      <!-- Заголовки колонок -->
      <div class="grid grid-cols-4 gap-4">
        <Skeleton class="h-5 w-24" />
        <Skeleton class="h-5 w-32" />
        <Skeleton class="h-5 w-20" />
        <Skeleton class="h-5 w-12" />
      </div>
  
      <!-- Строки таблицы -->
      <div v-for="n in 5" :key="n" class="grid grid-cols-4 gap-4">
        <Skeleton class="h-6 w-24" />
        <Skeleton class="h-6 w-32" />
        <Skeleton class="h-6 w-20" />
        <Skeleton class="h-6 w-12" />
      </div>
    </div>
  </template>

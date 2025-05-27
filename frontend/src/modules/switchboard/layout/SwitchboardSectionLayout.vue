<script setup lang="ts">
import { Separator } from '@/shared/ui/separator'
defineProps<{
  title: string
  description?: string
  withSeparator?: boolean
}>()
</script>

<template>
  <section class="space-y-3">
    <!-- Optional separator -->
    <Separator v-if="withSeparator" class="mt-12 mb-6 opacity-50" />

    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <div class="space-y-1">
        <h2 class="text-xl font-semibold tracking-tight">
          {{ title }}
        </h2>
        <p v-if="description" class="text-muted-foreground max-w-2xl text-sm leading-snug">
          {{ description }}
        </p>
      </div>
    </div>

    <!-- Main content -->
    <div>
      <slot />
    </div>

    <!-- Optional footer -->
    <div v-if="$slots.footer" class="mt-4">
      <slot name="footer" />
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
}>()
</script>

<template>
  <div>
    <div v-if="title" class="text-muted-foreground -mb-2 font-semibold tracking-tight">
      {{ title }}
    </div>

    <div class="flex flex-wrap items-center justify-between gap-4 pt-1 pb-4">
      <div class="flex flex-nowrap items-center gap-4">
        <slot name="filters" />
      </div>
      <div class="flex flex-wrap items-center gap-4">
        <slot name="buttons" />
      </div>
    </div>

    <slot name="table" />

    <div class="pt-2">
      <slot name="footer" />
    </div>
  </div>
</template>

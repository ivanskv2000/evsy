<script setup lang="ts">
</script>

<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-4 py-4">
      <div class="flex flex-nowrap items-center gap-4">
        <slot name="filters" />
      </div>
      <div class="flex flex-wrap items-center gap-4">
        <slot name="buttons" />
      </div>
    </div>

    <slot name="table" />

    <div class="py-4">
      <slot name="footer" />
    </div>
  </div>
</template>

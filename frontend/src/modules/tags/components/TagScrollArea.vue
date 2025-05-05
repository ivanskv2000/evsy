<script setup lang="ts">
import { useAttrs, computed } from 'vue'
import { cn } from '@/shared/utils/general'
import type { ClassValue } from 'clsx'

const attrs = useAttrs()

const wrapperClass = computed(() =>
  cn('tag-scroll-wrapper max-w-60', attrs.class as ClassValue)
)
</script>

<template>
  <div :class="wrapperClass" v-bind="{ ...attrs, class: undefined }">
    <div class="hide-scrollbar scroll-x-bounce flex flex-row gap-1 overflow-x-auto px-4">
      <slot />
    </div>
  </div>
</template>

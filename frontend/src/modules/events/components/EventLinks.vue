<script setup lang="ts">
import type { EventLink } from '@/modules/events/types'
import { Icon } from '@iconify/vue'

defineProps<{
  links: EventLink[]
}>()

const iconMap: Record<string, string> = {
  figma: 'simple-icons:figma',
  miro: 'simple-icons:miro',
  confluence: 'simple-icons:confluence',
  notion: 'simple-icons:notion',
  loom: 'simple-icons:loom',
  slack: 'simple-icons:slack',
  google: 'simple-icons:google',
  other: 'radix-icons:external-link',
}

function getLabel(link: EventLink): string {
  if (link.label) return link.label
  try {
    return new URL(link.url).hostname
  } catch {
    return link.url
  }
}
</script>

<template>
  <div class="flex flex-wrap items-center gap-3">
    <template v-for="(link, i) in links" :key="i">
      <a
        :href="link.url"
        target="_blank"
        rel="noopener noreferrer"
        class="hover:text-primary flex items-center gap-1 underline underline-offset-2 transition"
      >
        <Icon :icon="iconMap[link.type]" class="h-4 w-4" />
        <span>{{ getLabel(link) }}</span>
      </a>
    </template>
  </div>
</template>

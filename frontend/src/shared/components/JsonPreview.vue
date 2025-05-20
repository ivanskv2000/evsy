<script setup lang="ts">
import { computed } from 'vue'
import { useClipboard } from '@vueuse/core'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Icon } from '@iconify/vue'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/shared/ui/tooltip'
import type { JsonValue } from '@/modules/fields/types'

const props = defineProps<{
  value: JsonValue
  maxKeys?: number
}>()

function getJsonPreview(value: JsonValue, maxKeys = 2): string {
  if (value === null) return 'null'
  if (typeof value === 'number') return JSON.stringify(value.toFixed(1))
  if (typeof value !== 'object') return JSON.stringify(value)
  if (Array.isArray(value)) {
    const preview = value
      .slice(0, maxKeys)
      .map(v => getJsonPreview(v, 1))
      .join(', ')
    const suffix = value.length > maxKeys ? ', ...' : ''
    return `[${preview}${suffix}]`
  }

  const entries = Object.entries(value)
  const limited = entries.slice(0, maxKeys)

  const formatted = limited
    .map(([key, val]) => {
      return `${key}: ${getJsonPreview(val, 1)}`
    })
    .join(', ')

  const suffix = entries.length > maxKeys ? ', ...' : ''
  return `{ ${formatted}${suffix} }`
}

const shortPreview = computed(() => getJsonPreview(props.value, props.maxKeys))
const prettyJson = computed(() => JSON.stringify(props.value, null, 2))
const isShort = computed(() => shortPreview.value === prettyJson.value)

const { copy: copyJson, isSupported } = useClipboard({ source: prettyJson })
const { showCopied, showCopyError } = useEnhancedToast()

const handleCopyJson = async () => {
  try {
    await copyJson()
    showCopied('JSON')
  } catch {
    showCopyError('JSON')
  }
}
</script>

<template>
  <TooltipProvider :delay-duration="200">
    <Tooltip>
      <TooltipTrigger>
        <div class="font-mono">{{ shortPreview }}</div>
      </TooltipTrigger>
      <TooltipContent
        v-if="!isShort"
        side="bottom"
        @click.stop
        class="max-h-64 overflow-y-auto text-left text-xs"
      >
        <button
          v-if="isSupported"
          @click="handleCopyJson"
          class="text-muted-foreground absolute top-2 right-2 cursor-pointer text-[10px]"
        >
          <Icon icon="radix-icons:copy" class="mr-1 inline h-3 w-3" />
        </button>
        <div class="font-mono leading-snug whitespace-pre-wrap select-text">
          {{ prettyJson }}
        </div>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
</template>

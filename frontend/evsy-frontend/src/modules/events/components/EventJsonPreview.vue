<script setup lang="ts">
import { computed } from 'vue'
import { useClipboard } from '@vueuse/core'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Icon } from '@iconify/vue'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/shared/components/ui/tooltip'

const exampleValue = {
  user_id: 123,
  event_date: '2021-01-01',
  event_time: '2021-01-01T00:00:00Z',
  device: 'mobile',
  metadata: {
    source: 'landing',
    campaign: 'spring_sale',
  },
}

function getJsonPreview(obj: object, maxKeys = 2): string {
  const entries = Object.entries(obj)
  const limited = entries.slice(0, maxKeys)

  const formatted = limited
    .map(([key, value]) => {
      const val =
        typeof value === 'string' ? `"${value}"` : typeof value === 'object' ? '{...}' : value
      return `${key}: ${val}`
    })
    .join(', ')

  const suffix = entries.length > maxKeys ? ', ...' : ''
  return `{ ${formatted}${suffix} }`
}

const exampleShortPreview = computed(() => getJsonPreview(exampleValue))
const examplePrettyJson = computed(() => JSON.stringify(exampleValue, null, 2))

const { copy: copyJson, isSupported } = useClipboard({ source: examplePrettyJson })
const { showCopied, showCopyError } = useEnhancedToast()

const handleCopyJson = async () => {
  try {
    await copyJson()
    showCopied('Example')
  } catch (err) {
    showCopyError('Example')
  }
}
</script>

<template>
  <TooltipProvider :delay-duration="200">
    <Tooltip>
      <TooltipTrigger>
        <div class="flex items-center gap-2">
          <Icon icon="radix-icons:file-text" class="h-4 w-4" />
          <span>Example: <span class="font-mono">{{ exampleShortPreview }}</span></span>
        </div>
      </TooltipTrigger>
      <TooltipContent
        side="bottom"
        @click.stop
        class="max-h-64 overflow-y-auto text-left text-xs"
      >
        <button
          v-if="isSupported"
          @click="handleCopyJson"
          class="text-muted-foreground absolute top-2 right-2 text-[10px] hover:underline"
        >
          <Icon icon="radix-icons:copy" class="mr-1 inline h-3 w-3" />
        </button>
        <div class="font-mono leading-snug whitespace-pre-wrap select-text">
          {{ examplePrettyJson }}
        </div>
      </TooltipContent>
    </Tooltip>
  </TooltipProvider>
</template> 
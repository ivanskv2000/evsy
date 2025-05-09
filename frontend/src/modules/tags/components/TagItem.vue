<script setup lang="ts">
import { Button } from '@/shared/ui/button'
import { Badge } from '@/shared/ui/badge'
import { useClipboard } from '@vueuse/core'
import { Icon } from '@iconify/vue'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/shared/ui/tooltip'
import type { Tag } from '@/modules/tags/types'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

const props = defineProps<{
  tag: Tag
}>()

const emit = defineEmits<{
  (e: 'updateMe', id: string): void
  (e: 'deleteMe', id: string): void
}>()

const { copy: copyId } = useClipboard({ source: props.tag.id })
const { showCopied, showCopyError } = useEnhancedToast()

const handleCopyId = async () => {
  try {
    await copyId()
    showCopied('Tag')
  } catch {
    showCopyError('Tag')
  }
}
</script>

<template>
  <Transition name="fade" appear>
    <div
      class="flex items-start justify-between gap-4 rounded-lg border p-4 hover:shadow-sm transition-shadow"
    >
      <div>
        <TooltipProvider :delay-duration="800">
          <Tooltip>
            <TooltipTrigger>
              <Badge variant="secondary" class="cursor-pointer" @click="handleCopyId">
                <span class="font-mono">#{{ tag.id }}</span>
              </Badge>
            </TooltipTrigger>
            <TooltipContent>
              <p>Click to copy</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
        <p v-if="tag.description" class="text-muted-foreground mt-1 text-sm">
          {{ tag.description }}
        </p>
      </div>

      <div class="flex gap-2">
        <Button size="icon" variant="ghost" @click="emit('updateMe', tag.id)">
          <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
        </Button>
        <Button size="icon" variant="ghost" @click="emit('deleteMe', tag.id)">
          <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
        </Button>
      </div>
    </div>
  </Transition>
</template>

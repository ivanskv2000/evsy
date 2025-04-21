<script setup lang="ts">
import { Button } from '@/shared/components/ui/button'
import { Badge } from '@/shared/components/ui/badge'
import { useClipboard } from '@vueuse/core'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { Icon } from '@iconify/vue'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/shared/components/ui/tooltip'

const props = defineProps<{
  tag: { id: string; description?: string }
}>()

const { copy: copyId } = useClipboard({ source: props.tag.id })
const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
const { showInfoToast } = useInfoToast()

const handleCopyId = async () => {
  try {
    await copyId()
    showInfoToast('Tag copied to clipboard')
  } catch (err) {
    showApiErrorToast('Failed to copy Tag')
  }
}

</script>

<template>
  <div class="flex items-start justify-between gap-4 rounded-lg border p-4 transition hover:shadow-sm">
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
      <Button size="icon" variant="ghost" @click="">
        <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
      </Button>
      <Button size="icon" variant="ghost" @click="">
        <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
      </Button>
    </div>
  </div>
</template>

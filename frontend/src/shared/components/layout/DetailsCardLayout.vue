<script setup lang="ts">
import { useClipboard } from '@vueuse/core'
import { cn } from '@/shared/utils/general'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/shared/ui/card'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/shared/ui/tooltip'

const props = defineProps<{
  title: string
  description?: string
}>()

const { showCopied, showCopyError } = useEnhancedToast()
const { copy: copyTitle } = useClipboard({ source: props.title })

const handleCopyTitle = async () => {
  try {
    await copyTitle()
    showCopied('Name')
  } catch {
    showCopyError('Name')
  }
}
</script>

<template>
  <Transition name="fade" appear>
    <Card>
      <!-- Header -->
      <CardHeader>
        <div class="flex items-center justify-between">
          <!-- Title & Badge -->
          <div class="flex items-center space-x-2">
            <!-- Title -->
            <TooltipProvider :delay-duration="800">
              <Tooltip>
                <TooltipTrigger>
                  <CardTitle
                    :class="
                      cn(
                        'cursor-pointer font-mono text-xl leading-tight tracking-wide',
                        'max-w-[12ch] truncate overflow-hidden whitespace-nowrap sm:max-w-[36ch]'
                      )
                    "
                    @click="handleCopyTitle"
                  >
                    {{ title }}
                  </CardTitle>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Click to copy</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <!-- Badge -->
            <slot name="badge" />
          </div>

          <!-- Action Buttons -->
          <div class="flex space-x-2">
            <slot name="actions" />
          </div>
        </div>

        <!-- Description -->
        <CardDescription v-if="description">
          {{ description }}
        </CardDescription>

        <!-- Attributes -->
        <div class="text-muted-foreground mt-4 space-y-3 text-sm">
          <slot name="attributes" />
        </div>
      </CardHeader>

      <!-- Content -->
      <CardContent>
        <slot name="content" />
      </CardContent>

      <!-- Footer -->
      <CardFooter v-if="$slots.footer">
        <slot name="footer" />
      </CardFooter>
    </Card>
  </Transition>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useClipboard } from '@vueuse/core'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/shared/ui/dialog'
import { Label } from '@/shared/ui/label'
import { Button } from '@/shared/ui/button'
import { Switch } from '@/shared/ui/switch'
import { api } from '@/shared/utils/api'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  open: boolean
  eventId: number
  onClose: () => void
}>()

const settings = reactive({
  includeDescriptions: true,
  includeExamples: true,
  additionalProperties: true,
  format: 'yaml' as 'yaml' | 'json',
})

const preview = ref('')
const updates = ref(0)
const { run: fetchSchemaPreview, isLoading } = useAsyncTask()

const { copy: copyJson, isSupported } = useClipboard({ source: preview })
const { showCopied, showCopyError } = useEnhancedToast()
const handleCopy = async () => {
  try {
    await copyJson()
    showCopied('Schema')
  } catch {
    showCopyError('Schema')
  }
}

function handleFetch() {
  const params = {
    include_descriptions: settings.includeDescriptions,
    include_examples: settings.includeExamples,
    additional_properties: settings.additionalProperties,
  }
  const format = settings.format

  fetchSchemaPreview(async () => {
    const response = await api.get(`/events/${props.eventId}/schema.${format}`, {
      params,
      responseType: 'text',
    })

    preview.value =
      format === 'json' ? JSON.stringify(JSON.parse(response.data), null, 2) : response.data
    updates.value += 1
  })
}

watch(
  () => props.open,
  isOpen => {
    if (isOpen) {
      preview.value = ''
      handleFetch()
    }
  },
  { immediate: true }
)
</script>

<template>
  <Dialog :open="props.open" @update:open="props.onClose">
    <DialogContent class="!max-w-4xl">
      <DialogHeader>
        <DialogTitle>Export Schema</DialogTitle>
        <DialogDescription>
          Generate a Swagger schema for the event. You can customize the settings below to include
          or exclude certain properties.
        </DialogDescription>
      </DialogHeader>

      <div class="mt-4 grid grid-cols-1 gap-8 md:grid-cols-[1fr_2fr]">
        <!-- Settings Column -->
        <div class="space-y-6">
          <div class="flex items-center justify-between">
            <Label for="includeDescriptions">Include descriptions</Label>
            <Switch id="includeDescriptions" v-model="settings.includeDescriptions" />
          </div>

          <div class="flex items-center justify-between">
            <Label for="includeExamples">Include examples</Label>
            <Switch id="includeExamples" v-model="settings.includeExamples" />
          </div>

          <div class="flex items-center justify-between">
            <Label for="additionalProperties">Allow additional properties</Label>
            <Switch id="additionalProperties" v-model="settings.additionalProperties" />
          </div>

          <div class="mt-12 flex items-center justify-between">
            <Label for="format">Schema format</Label>
            <div class="flex gap-2">
              <Button
                class="w-16 font-mono"
                :variant="settings.format === 'yaml' ? 'default' : 'outline'"
                size="sm"
                @click="settings.format = 'yaml'"
              >
                YAML
              </Button>
              <Button
                class="w-16 font-mono"
                :variant="settings.format === 'json' ? 'default' : 'outline'"
                size="sm"
                @click="settings.format = 'json'"
              >
                JSON
              </Button>
            </div>
          </div>

          <div>
            <Button variant="secondary" class="w-full" @click="handleFetch" :disabled="isLoading">
              Update
            </Button>
          </div>
        </div>

        <!-- Preview Column -->
        <div>
          <!-- <Textarea class="h-[400px] resize-none font-mono text-sm" :value="preview" readonly /> -->

          <div
            side="bottom"
            @click.stop
            class="relative border-muted-foreground bg-foreground text-background h-[400px] overflow-y-auto rounded-md border p-4 text-left shadow-sm"
          >
            <button
              v-if="isSupported"
              @click="handleCopy"
              class="text-muted-foreground absolute top-2 right-2 cursor-pointer text-[10px]"
            >
              <Icon icon="radix-icons:copy" class="mr-1 inline h-3 w-3" />
            </button>
            <Transition name="fade-slide" mode="out-in">
              <div :key="updates" class="font-mono leading-snug whitespace-pre-wrap select-text">
                {{ preview }}
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>

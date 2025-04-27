<script setup lang="ts">
import { ref } from 'vue'
import type { Event } from '@/modules/events/types'
import { Button } from '@/shared/components/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/shared/components/ui/card'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/shared/components/ui/tooltip'
import { useRouter } from 'vue-router'
import { useClipboard } from '@vueuse/core'
import { Badge } from '@/shared/components/ui/badge'
import { Icon } from '@iconify/vue'
import EventFieldsTable from './EventFieldsTable.vue'
import JsonPreview from '@/shared/components/JsonPreview.vue'

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

const router = useRouter()
const { showCopied, showCopyError } = useEnhancedToast()

const props = defineProps<{
  event: Event
  loading: {
    isSaving: boolean
    isDeleting: boolean
  }
}>()

const emit = defineEmits<{
  (e: 'update', values: EventFormValues): void
  (e: 'delete'): void
}>()

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const submitEdit = (values: EventFormValues) => {
  emit('update', values)
  showEditModal.value = false
}

const confirmDelete = () => {
  emit('delete')
  showDeleteModal.value = false
}

const { copy: copyId } = useClipboard({ source: props.event.id.toString() })
const { copy: copyName } = useClipboard({ source: props.event.name })

const handleCopyId = async () => {
  try {
    await copyId()
    showCopied('ID')
  } catch (err) {
    showCopyError('ID')
  }
}

const handleCopyName = async () => {
  try {
    await copyName()
    showCopied('Name')
  } catch (err) {
    showCopyError('Name')
  }
}
</script>

<template>
  <Card>
    <CardHeader>
      <div class="flex items-center justify-between">
        <!-- Title & ID -->
        <div class="flex items-center space-x-2">
          <TooltipProvider :delay-duration="800">
            <Tooltip>
              <TooltipTrigger>
                <CardTitle class="cursor-pointer font-mono text-xl tracking-wide" @click="handleCopyName">
                  {{ event.name }}
                </CardTitle>
              </TooltipTrigger>
              <TooltipContent>
                <p>Click to copy</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider :delay-duration="800">
            <Tooltip>
              <TooltipTrigger>
                <Badge variant="outline" class="cursor-pointer text-xs tracking-wide" @click="handleCopyId">
                  ID: {{ event.id }}
                </Badge>
              </TooltipTrigger>
              <TooltipContent>
                <p>Click to copy</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>

        <!-- Edit & Delete -->
        <div class="flex space-x-2">
          <Button size="icon" variant="ghost" @click="showEditModal = true">
            <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
          </Button>
          <Button size="icon" variant="ghost" @click="showDeleteModal = true">
            <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
          </Button>
        </div>
      </div>

      <CardDescription v-if="event.description">
        {{ event.description }}
      </CardDescription>

      <!-- Details section -->
      <div class="text-muted-foreground mt-4 space-y-3 text-sm">

        <!-- Tags -->
        <div v-if="event.tags.length > 0" class="flex flex-wrap items-center gap-1">
          <div class="flex items-center gap-1">
            <Icon icon="radix-icons:component-1" class="h-4 w-4" />
            <span>Tags:</span>
          </div>
          <Badge v-for="tag in event.tags" :key="tag.id" variant="secondary" class="font-mono tracking-wide">
            {{ tag.id }}
          </Badge>
        </div>

        <!-- Example -->
        <div class="flex flex-wrap items-center gap-1">
          <div class="flex items-center gap-1">
            <Icon icon="radix-icons:file-text" class="h-4 w-4" />
            <span>Example:</span>
          </div>
          <JsonPreview :value="exampleValue" />
        </div>
      </div>
    </CardHeader>

    <CardContent>
      <EventFieldsTable :fields="event.fields" />
    </CardContent>

    <!-- Modals -->
    <EventEditModal :open="showEditModal" :event="event" :onClose="() => (showEditModal = false)" :onSubmit="submitEdit"
      :isSaving="loading.isSaving" />
    <DeleteModal :open="showDeleteModal" :onClose="() => (showDeleteModal = false)" :onConfirm="confirmDelete"
      :isDeleting="loading.isDeleting" />
  </Card>
</template>

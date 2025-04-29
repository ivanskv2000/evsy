<script setup lang="ts">
import { ref } from 'vue'
import type { Event } from '@/modules/events/types'
import { Button } from '@/shared/components/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { EventFormValues } from '@/modules/events/validation/eventSchema'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
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
import DetailsCardLayout from '@/shared/components/layout/DetailsCardLayout.vue'
import DetailsCardAttribute from '@/shared/components/layout/DetailsCardAttribute.vue'

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

const handleCopyId = async () => {
  try {
    await copyId()
    showCopied('ID')
  } catch (err) {
    showCopyError('ID')
  }
}
</script>

<template>
  <div>
    <DetailsCardLayout :title="event.name" :description="event.description ?? undefined">
      <template #badge>
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
      </template>

      <template #actions>
        <Button size="icon" variant="ghost" @click="showEditModal = true">
          <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
        </Button>
        <Button size="icon" variant="ghost" @click="showDeleteModal = true">
          <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
        </Button>
      </template>

      <template #attributes>
        <!-- Tags -->
        <DetailsCardAttribute v-if="event.tags.length > 0" icon="ph:tag" label="Tags">
          <template #value>
            <Badge v-for="tag in event.tags" :key="tag.id" variant="secondary" class="font-mono tracking-wide">
              {{ tag.id }}
            </Badge>
          </template>
        </DetailsCardAttribute>

        <!-- Example -->
        <DetailsCardAttribute icon="radix-icons:file-text" label="Example">
          <template #value>
            <JsonPreview :value="exampleValue" />
          </template>
        </DetailsCardAttribute>
      </template>

      <template #content>
        <EventFieldsTable :fields="event.fields" />
      </template>
    </DetailsCardLayout>

    <!-- Modals -->
    <EventEditModal :open="showEditModal" :event="event" :onClose="() => (showEditModal = false)" :onSubmit="submitEdit"
      :isSaving="loading.isSaving" />
    <DeleteModal :open="showDeleteModal" :onClose="() => (showDeleteModal = false)" :onConfirm="confirmDelete"
      :isDeleting="loading.isDeleting" />
  </div>
</template>

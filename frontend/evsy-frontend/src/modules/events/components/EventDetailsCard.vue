<script setup lang="ts">
import { ref } from 'vue'
import type { Event } from '@/modules/events/types'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/shared/components/ui/card'
import { Badge } from '@/shared/components/ui/badge'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/components/ui/button'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
import DeleteModal from '@/shared/components/data/DeleteModal.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { eventApi } from '@/modules/events/api'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { useRouter } from 'vue-router'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/shared/components/ui/tooltip'
import { useClipboard } from '@vueuse/core'

const props = defineProps<{
  event: Event
}>()

const emit = defineEmits<{
  (e: 'updated', event: Event): void
}>()

const router = useRouter()
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()
const { showSuccessToast } = useSuccessToast()
const { showApiErrorToast } = useApiErrorToast()
const { showInfoToast } = useInfoToast()

const handleUpdate = (updatedEvent: Event) => {
  emit('updated', updatedEvent)
}

const handleDelete = () => {
  runDeleteTask(async () => {
    await eventApi.delete(props.event.id)
    showSuccessToast('Event deleted successfully!')
    showDeleteModal.value = false
    router.push('/events')
  })
}


const { copy: copyId } = useClipboard({ source: props.event.id.toString() })
const { copy: copyName } = useClipboard({ source: props.event.name })

const handleCopyId = async () => {
  try {
    await copyId()
    showInfoToast('ID copied to clipboard')
  } catch (err) {
    showApiErrorToast('Failed to copy ID')
  }
}

const handleCopyName = async () => {
  try {
    await copyName()
    showInfoToast('Name copied to clipboard')
  } catch (err) {
    showApiErrorToast('Failed to copy name')
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
          <Badge variant="outline" class="text-xs tracking-wide cursor-pointer" @click="handleCopyId">
            ID: {{ event.id }}
        </Badge>
        </div>

        <!-- Edit & Delete buttons -->
        <div class="flex space-x-2">
          <Button size="icon" variant="ghost" @click="showEditModal = true">
            <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
          </Button>
          <Button size="icon" variant="ghost" @click="showDeleteModal = true">
            <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
          </Button>
        </div>
      </div>

      <CardDescription v-if="event.description" class="mt-2">
        {{ event.description }}
      </CardDescription>

      <div class="mt-4 flex flex-wrap items-center gap-2">
        <div class="flex items-center gap-1">
          <Icon icon="radix-icons:component-1" class="w-4 h-4 text-muted-foreground" />
          <span class="text-sm text-muted-foreground">Tags:</span>
        </div>
        <Badge
          v-for="tag in event.tags"
          :key="tag.id"
          variant="secondary"
          class="text-xs uppercase tracking-wide"
        >
          {{ tag.id }}
        </Badge>
      </div>

      <div class="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
        <Icon icon="radix-icons:file-text" class="h-4 w-4" />
        <span>Example: <span class="font-mono">{"..."}</span></span>
      </div>
    </CardHeader>

    <CardContent>
      <div class="mt-4">
        <h3 class="mb-2 text-sm font-semibold text-muted-foreground">Associated Fields</h3>
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left border border-muted rounded-md">
            <thead class="bg-muted/50">
              <tr>
                <th class="px-3 py-2">Name</th>
                <th class="px-3 py-2">Type</th>
                <th class="px-3 py-2">Description</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="field in event.fields"
                :key="field.id"
                class="border-t border-muted"
              >
                <td class="px-3 py-2 font-mono">{{ field.name }}</td>
                <td class="px-3 py-2 capitalize">{{ field.field_type }}</td>
                <td class="px-3 py-2 text-muted-foreground">
                  {{ field.description || '—' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </CardContent>

    <!-- Modals -->
    <EventEditModal
      v-if="showEditModal"
      :event="event"
      @close="showEditModal = false"
      @updated="handleUpdate"
    />
    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="handleDelete"
      :isDeleting="isDeleting"
      description="Once deleted, this event will be unlinked from any tags or fields it's associated with."
    />
  </Card>
</template>

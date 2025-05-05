<script setup lang="ts">
import { useClipboard } from '@vueuse/core'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import type { Event } from '@/modules/events/types'
import { Button } from '@/shared/ui/button'
import { Badge } from '@/shared/ui/badge'
import { Icon } from '@iconify/vue'
import EventFieldsTable from './EventFieldsTable.vue'
import JsonPreview from '@/shared/components/JsonPreview.vue'
import DetailsCardLayout from '@/shared/components/layout/DetailsCardLayout.vue'
import DetailsCardAttribute from '@/shared/components/layout/DetailsCardAttribute.vue'
import { getEventFieldsColumns } from '@/modules/events/components/eventFieldsColumns'
import TagScrollArea from '@/modules/tags/components/TagScrollArea.vue'

const eventExample = {
  user_id: 12,
  event_date: '2024-01-01',
  event_time: '2024-01-01T00:00:00Z',
  device: 'mobile',
  metadata: {
    source: 'landing',
    campaign: 'spring_sale',
  },
}

const props = defineProps<{
  event: Event
}>()

const emit = defineEmits<{
  (e: 'edit'): void
  (e: 'delete'): void
}>()

const { showCopied, showCopyError } = useEnhancedToast()
const { copy: copyId } = useClipboard({ source: props.event.id.toString() })

const handleCopyId = async () => {
  try {
    await copyId()
    showCopied('ID')
  } catch {
    showCopyError('ID')
  }
}

const columns = getEventFieldsColumns()
</script>

<template>
  <div>
    <DetailsCardLayout :title="event.name" :description="event.description ?? undefined">
      <template #badge>
        <Badge variant="outline" class="cursor-pointer text-xs tracking-wide" @click="handleCopyId">
          ID: {{ event.id }}
        </Badge>
      </template>

      <template #actions>
        <Button size="icon" variant="ghost" @click="emit('edit')">
          <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
        </Button>
        <Button size="icon" variant="ghost" @click="emit('delete')">
          <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
        </Button>
      </template>

      <template #attributes>
        <!-- Tags -->
        <DetailsCardAttribute v-if="event.tags.length > 0" icon="ph:tag" label="Tags">
          <template #value>
            <TagScrollArea class="max-w-lg">
              <Badge
                v-for="tag in event.tags"
                :key="tag.id"
                variant="secondary"
                class="font-mono tracking-wide"
              >
                {{ tag.id }}
              </Badge>
            </TagScrollArea>
          </template>
        </DetailsCardAttribute>

        <!-- Example -->
        <DetailsCardAttribute icon="radix-icons:file-text" label="Example">
          <template #value>
            <JsonPreview :value="eventExample" />
          </template>
        </DetailsCardAttribute>
      </template>

      <template #content>
        <div class="container mx-auto mt-4">
          <EventFieldsTable
            title="Associated fields"
            :columns="columns"
            :data="event.fields"
            :isLoading="false"
          />
        </div>
      </template>
    </DetailsCardLayout>
  </div>
</template>

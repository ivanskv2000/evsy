<script setup lang="ts">
import type { Field } from '@/modules/fields/types'
import { Button } from '@/shared/ui/button'
import { Badge } from '@/shared/ui/badge'
import { Icon } from '@iconify/vue'
import JsonPreview from '@/shared/components/JsonPreview.vue'
import DetailsCardLayout from '@/shared/components/layout/DetailsCardLayout.vue'
import DetailsCardAttribute from '@/shared/components/layout/DetailsCardAttribute.vue'
import DetailsCardSkeleton from '@/shared/components/skeletons/DetailsCardSkeleton.vue'

defineProps<{
  field: Field
  isLoading: boolean
}>()

const emit = defineEmits(['edit-clicked', 'delete-clicked'])
</script>

<template>
  <div>
    <DetailsCardSkeleton v-if="isLoading" />
    <DetailsCardLayout v-else :title="field.name" :description="field.description ?? undefined">
      <template #badge>
        <Badge variant="secondary" class="text-xs tracking-wide uppercase">
          {{ field.field_type }}
        </Badge>
      </template>

      <template #actions>
        <Button size="icon" variant="ghost" @click="emit('edit-clicked')">
          <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
        </Button>
        <Button size="icon" variant="ghost" @click="emit('delete-clicked')">
          <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
        </Button>
      </template>

      <template #attributes>
        <DetailsCardAttribute icon="radix-icons:id-card" label="ID" :value="field.id.toString()" />

        <DetailsCardAttribute v-if="field.example" icon="radix-icons:file-text" label="Example">
          <template #value>
            <JsonPreview :value="field.example" />
          </template>
        </DetailsCardAttribute>

        <DetailsCardAttribute icon="radix-icons:bar-chart" label="Used in">
          <template #value>
            {{ `${field.event_count || 0} events` }}
          </template>
        </DetailsCardAttribute>
      </template>
    </DetailsCardLayout>
  </div>
</template>

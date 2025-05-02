<script setup lang="ts">
import { ref } from 'vue'
import type { Field } from '@/modules/fields/types'
import { Button } from '@/shared/ui/button'
import type { FieldFormValues } from '@/modules/fields/validation/fieldSchema'
import DeleteModal from '@/shared/components/modals/DeleteModal.vue'
import FieldEditModal from '@/modules/fields/components/FieldEditModal.vue'
import { Badge } from '@/shared/ui/badge'
import { Icon } from '@iconify/vue'
import JsonPreview from '@/shared/components/JsonPreview.vue'
import DetailsCardLayout from '@/shared/components/layout/DetailsCardLayout.vue'
import DetailsCardAttribute from '@/shared/components/layout/DetailsCardAttribute.vue'
import DetailsCardSkeleton from '@/shared/components/skeletons/DetailsCardSkeleton.vue'

defineProps<{
  field: Field
  loading: {
    isLoading: boolean
    isSaving: boolean
    isDeleting: boolean
  }
}>()

const emit = defineEmits<{
  (e: 'update', values: FieldFormValues): void
  (e: 'delete'): void
}>()

const showEditModal = ref(false)
const showDeleteModal = ref(false)

const submitEdit = (values: FieldFormValues) => {
  emit('update', values)
  showEditModal.value = false
}

const confirmDelete = () => {
  emit('delete')
  showDeleteModal.value = false
}
</script>

<template>
  <div>
    <DetailsCardSkeleton v-if="loading.isLoading"/>
    <DetailsCardLayout v-else :title="field.name" :description="field.description ?? undefined">
      <template #badge>
        <Badge variant="secondary" class="text-xs tracking-wide uppercase">
          {{ field.field_type }}
        </Badge>
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
        <!-- ID -->
        <DetailsCardAttribute icon="radix-icons:id-card" label="ID" :value="field.id.toString()" />

        <!-- Example -->
        <DetailsCardAttribute v-if="field.example" icon="radix-icons:file-text" label="Example">
          <template #value>
            <JsonPreview :value="field.example" />
          </template>
        </DetailsCardAttribute>

        <!-- Used in -->
        <DetailsCardAttribute icon="radix-icons:bar-chart" label="Used in">
          <template #value>
            {{ `${field.event_count || 0} events` }}
          </template>
        </DetailsCardAttribute>
      </template>
    </DetailsCardLayout>

    <!-- Modals -->
    <FieldEditModal
      :open="showEditModal"
      :field="field"
      :onClose="() => (showEditModal = false)"
      :onSubmit="submitEdit"
      :isSaving="loading.isSaving"
    />
    <DeleteModal
      :open="showDeleteModal"
      :onClose="() => (showDeleteModal = false)"
      :onConfirm="confirmDelete"
      :isDeleting="loading.isDeleting"
      description="Once deleted, this field will be unlinked from any events it's part of."
    />
  </div>
</template>

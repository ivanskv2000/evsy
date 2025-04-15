<template>
  <DefaultLayout>
    <template #actions>
      <Button variant="outline">+ Add Field</Button>
    </template>

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="field in fields" :key="field.id" class="border rounded-xl p-4 bg-card">
        <h2 class="text-lg font-semibold">{{ field.name }}</h2>
        <p class="text-muted-foreground text-sm">{{ field.description || 'No description' }}</p>
        <p class="text-xs mt-2"><strong>Type:</strong> {{ field.field_type }}</p>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layout/DefaultLayout.vue'
import { Button } from '@/components/ui/button'
import { ref, onMounted } from 'vue'
import { api } from '@/lib/api'
import type { Field } from '@/types'

const fields = ref<Field[]>([])

onMounted(async () => {
  fields.value = await api.get<Field[]>('/fields')
})
</script>
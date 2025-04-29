<script setup lang="ts">
import type { Event } from '@/modules/events/types'
import { RouterLink } from 'vue-router'

defineProps<{
  fields: Event['fields']
}>()
</script>

<template>
  <div class="mt-4">
    <h3 class="text-muted-foreground mb-2 text-sm font-semibold">Associated Fields</h3>
    <div class="overflow-x-auto">
      <table class="border-muted w-full rounded-md border text-left text-sm">
        <thead class="bg-muted/50">
          <tr>
            <th class="px-3 py-2">Name</th>
            <th class="px-3 py-2">Type</th>
            <th class="px-3 py-2">Description</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="field in fields"
            :key="field.id"
            class="border-muted hover:bg-muted/30 border-t"
          >
            <RouterLink :to="`/fields/${field.id}`" class="contents">
              <td class="px-3 py-2 font-mono">{{ field.name }}</td>
              <td class="px-3 py-2 capitalize">{{ field.field_type }}</td>
              <td class="text-muted-foreground px-3 py-2">
                {{ field.description || '—' }}
              </td>
            </RouterLink>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

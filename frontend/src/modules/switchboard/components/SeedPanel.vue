<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { seedDatabase } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

const queryClient = useQueryClient()
const { showSuccess } = useEnhancedToast()

const { mutate: handleSeed, isPending: isLoading } = useMutation({
  mutationFn: () => seedDatabase(),
  onSuccess: () => {
    showSuccess('Database seeded successfully')
    // Invalidate all queries to force a refetch across the app,
    // ensuring components like the ResetPanel preview are updated.
    queryClient.invalidateQueries()
  },
})
</script>

<template>
  <SwitchboardSection
    title="Seed database"
    description="Populate the database with example tags, fields, and events. Works on an empty database only."
    :with-separator="true"
  >
    <template #default>
      <Button :disabled="isLoading" @click="handleSeed"> Seed </Button>
    </template>
  </SwitchboardSection>
</template>

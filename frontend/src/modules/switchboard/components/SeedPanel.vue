<script setup lang="ts">
import SwitchboardSection from '../layout/SwitchboardSectionLayout.vue'
import { seedDatabase } from '../api'
import { Button } from '@/shared/ui/button'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'

const { run, isLoading } = useAsyncTask()
const { showSuccess } = useEnhancedToast()

const handleSeed = () => {
  run(async () => {
    await seedDatabase()
    showSuccess('Database seeded successfully')
  })
}
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

<script setup lang="ts">
import UserSection from '../layout/UserSectionLayout.vue'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'

const auth = useAuthStore()
</script>

<template>
  <UserSection :with-separator="true">
    <template #default>
      <div class="mb-6">
        <p class="text-muted-foreground max-w-2xl text-sm leading-snug">Logged in as</p>
        <p class="text-lg font-medium">{{ auth.email }}</p>
      </div>
    </template>
  </UserSection>
</template>

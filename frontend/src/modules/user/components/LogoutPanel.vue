<script setup lang="ts">
import UserSection from '../layout/UserSectionLayout.vue'
import LogoutButton from '@/modules/auth/components/LogoutButton.vue'
</script>

<template>
  <UserSection
    title="Log out"
    description="Evsy is only available to you when you are logged in. If you log out, you will not be able to access your events and other data."
    :with-separator="true"
  >
    <template #default>
      <LogoutButton />
    </template>
  </UserSection>
</template>

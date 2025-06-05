<script setup lang="ts">
import Header from '@/shared/components/layout/PageHeader.vue'
import UserInfoPanel from '../components/UserInfoPanel.vue'
import LogoutPanel from '../components/LogoutPanel.vue'
</script>

<template>
  <div>
    <Header title="Profile" />
    <div class="container mx-auto">
      <div class="mb-24 space-y-12">
        <UserInfoPanel :with-separator="false" />
        <LogoutPanel />
      </div>
    </div>
  </div>
</template>

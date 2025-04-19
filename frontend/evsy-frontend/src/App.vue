<script setup lang="ts">
import { RouterView } from 'vue-router'
import MainLayout from '@/shared/components/layout/MainLayout.vue'
import { Toaster } from '@/shared/components/ui/sonner'
</script>

<template>
  <Toaster richColors />
  <MainLayout>
    <RouterView />
  </MainLayout>
</template>


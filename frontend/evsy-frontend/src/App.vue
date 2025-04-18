<script setup lang="ts">
import { RouterView } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
import { Toaster } from '@/components/ui/sonner'
</script>

<template>
  <Toaster richColors />
  <MainLayout>
    <RouterView />
  </MainLayout>
</template>


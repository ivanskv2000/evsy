<script setup lang="ts">
import { RouterView } from 'vue-router'
import MainLayout from '@/shared/components/layout/MainLayout.vue'
import { Toaster } from '@/shared/components/ui/sonner'
import { Transition } from 'vue'
</script>

<template>
  <Toaster richColors />
  <MainLayout>
    <!-- <RouterView /> -->
      <Transition
        name="page"
        mode="out-in"
        appear
      >
        <RouterView />
      </Transition>
  </MainLayout>
</template>


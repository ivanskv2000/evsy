<script setup lang="ts">
import { RouterView } from 'vue-router'
import MainLayout from '@/shared/components/layout/MainLayout.vue'
import { Toaster } from '@/shared/ui/sonner'
import { Transition } from 'vue'
</script>

<template>
  <Toaster richColors />
  <MainLayout>
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in" appear>
        <component :is="Component" />
      </Transition>
    </RouterView>
  </MainLayout>
</template>

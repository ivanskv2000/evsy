<script setup lang="ts">
import MainLogo from '@/shared/components/layout/MainLogo.vue'
import NavigationMenu from '@/shared/components/layout/NavigationMenu.vue'
import DropdownMenu from '@/shared/components/layout/DropdownMenu.vue'
import LoveFooter from './LoveFooter.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col bg-background">
    <!-- Header -->
    <header class="bg-background sticky top-0 z-50 w-full border-b drop-shadow-accent">
      <div class="container flex h-14 items-center">
        <div class="flex">
          <MainLogo />
          <NavigationMenu />
        </div>
        <div class="flex flex-1 items-center justify-end space-x-2">
          <DropdownMenu />
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container py-6 flex-1">
      <slot />
    </main>

    <!-- Sticky Footer -->
    <LoveFooter />
  </div>
</template>

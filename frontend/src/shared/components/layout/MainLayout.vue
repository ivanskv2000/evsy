<script setup lang="ts">
import MainLogo from '@/shared/components/layout/MainLogo.vue'
import NavigationMenu from '@/shared/components/layout/NavigationMenu.vue'
import DropdownMenu from '@/shared/components/layout/DropdownMenu.vue'
import LoveFooter from './LoveFooter.vue'
</script>

<template>
  <div class="bg-background flex min-h-screen flex-col">
    <!-- Header -->
    <header class="bg-background drop-shadow-accent sticky top-0 z-50 w-full border-b">
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
    <main class="container flex-1 py-6">
      <slot />
    </main>

    <!-- Sticky Footer -->
    <LoveFooter />
  </div>
</template>

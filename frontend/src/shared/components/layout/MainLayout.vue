<script setup lang="ts">
import MainLogo from '@/shared/components/layout/MainLogo.vue'
import NavigationMenu from '@/shared/components/layout/NavigationMenu.vue'
import DropdownMenu from '@/shared/components/layout/DropdownMenu.vue'
import LoveFooter from './LoveFooter.vue'
import { useAppConfig } from '@/shared/composables/useAppConfig'
import LogoutButton from '@/modules/auth/components/LogoutButton.vue'
import LoginButton from '@/modules/auth/components/LoginButton.vue'

const { isDemo, isDev } = useAppConfig()
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
          <div v-if="isDev || isDemo" class="text-muted-foreground font-mono text-sm font-semibold">
            {{ isDev ? 'DEV' : 'DEMO' }}
          </div>
          <!-- Auth Buttons -->
          <LogoutButton />
          <LoginButton />
          <!-- Dropdown Menu -->
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

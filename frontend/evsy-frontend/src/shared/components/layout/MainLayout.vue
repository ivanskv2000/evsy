<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/shared/components/ui/button'
import { Icon } from '@iconify/vue'
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from '@/shared/components/ui/navigation-menu'
import ThemeProvider from '@/shared/components/providers/theme-provider.vue'
</script>

<template>
  <div class="bg-background min-h-screen">
    <!-- Header -->
    <header
      class="bg-background/95 supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50 w-full border-b backdrop-blur"
    >
      <div class="container flex h-14 items-center">
        <div class="mr-4 flex">
    <RouterLink to="/" class="mr-6 flex items-center space-x-2">
      <span class="font-handwritten text-xl">Evsy</span>
    </RouterLink>

    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuLink as-child>
            <RouterLink to="/events">Events</RouterLink>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink as-child>
            <RouterLink to="/fields">Fields</RouterLink>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink as-child>
            <RouterLink to="/tags">Tags</RouterLink>
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  </div>
        <div class="flex flex-1 items-center justify-end space-x-2">
          <ThemeProvider v-slot="{ toggleTheme }">
            <Button variant="ghost" size="icon" @click="toggleTheme">
              <Icon
                icon="radix-icons:moon"
                class="h-[1.2rem] w-[1.2rem] scale-100 rotate-0 transition-all dark:scale-0 dark:-rotate-90"
              />
              <Icon
                icon="radix-icons:sun"
                class="absolute h-[1.2rem] w-[1.2rem] scale-0 rotate-90 transition-all dark:scale-100 dark:rotate-0"
              />
              <span class="sr-only">Toggle theme</span>
            </Button>
          </ThemeProvider>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container py-6">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from '@/shared/ui/navigation-menu'
import ThemeProvider from '@/shared/components/providers/theme-provider.vue'
</script>

<template>
  <div class="bg-background min-h-screen">
    <!-- Header -->
    <header class="sticky top-0 w-full border-b">
      <div class="container flex h-14 items-center">
        <div class="flex">
          <RouterLink to="/" class="mr-6">
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
                class="h-4 w-4 scale-100 rotate-0 opacity-100 transition-all duration-300 ease-in-out dark:scale-0 dark:-rotate-90 dark:opacity-0"
              />
              <Icon
                icon="radix-icons:sun"
                class="absolute h-4 w-4 scale-0 rotate-90 opacity-0 transition-all duration-300 ease-in-out dark:scale-100 dark:rotate-0 dark:opacity-100"
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

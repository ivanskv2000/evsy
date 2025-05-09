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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu'
import ThemeProvider from '@/shared/components/providers/theme-provider.vue'
</script>

<template>
  <div class="bg-background min-h-screen">
    <!-- Header -->
    <header class="bg-background sticky top-0 z-50 w-full border-b">
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
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <Button
                variant="ghost"
                size="icon"
                class="group relative flex h-9 w-9 cursor-pointer items-center justify-center transition-none hover:bg-transparent hover:text-inherit dark:hover:bg-transparent dark:hover:text-inherit"
              >
                <span class="relative h-4 w-4">
                  <Icon
                    icon="radix-icons:hamburger-menu"
                    class="transition-rotate absolute inset-0 scale-100 rotate-0 opacity-100 transition-opacity transition-transform duration-300 ease-in-out group-data-[state=open]:scale-0 group-data-[state=open]:-rotate-90 group-data-[state=open]:opacity-0"
                  />
                  <Icon
                    icon="radix-icons:cross-1"
                    class="transition-rotate absolute inset-0 scale-0 rotate-90 opacity-0 transition-opacity transition-transform duration-300 ease-in-out group-data-[state=open]:scale-100 group-data-[state=open]:rotate-0 group-data-[state=open]:opacity-100"
                  />
                </span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent class="w-auto" align="end">
              <DropdownMenuGroup>
                <ThemeProvider v-slot="{ toggleTheme }">
                  <DropdownMenuItem
                    @click="toggleTheme"
                    @select.prevent
                    class="relative flex items-center justify-start"
                  >
                    <span class="relative mr-2 h-4 w-4">
                      <Icon
                        icon="radix-icons:moon"
                        class="absolute inset-0 scale-100 rotate-0 transform opacity-100 transition duration-300 ease-in-out dark:scale-0 dark:-rotate-90 dark:opacity-0"
                      />
                      <Icon
                        icon="radix-icons:sun"
                        class="absolute inset-0 scale-0 rotate-90 transform opacity-0 transition duration-300 ease-in-out dark:scale-100 dark:rotate-0 dark:opacity-100"
                      />
                    </span>
                    <span>Toggle theme</span>
                  </DropdownMenuItem>
                </ThemeProvider>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem as-child>
                  <a
                    href="https://github.com/ivanskv2000/evsy"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="flex items-center"
                  >
                    <Icon icon="simple-icons:github" class="mr-2 h-4 w-4" />
                    <span>GitHub source</span>
                  </a>
                </DropdownMenuItem>
                <DropdownMenuItem as-child>
                  <a
                    href="https://buymeacoffee.com/ivanskv2000"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="flex items-center"
                  >
                    <Icon icon="simple-icons:buymeacoffee" class="mr-2 h-4 w-4" />
                    <span>Buy me a coffee</span>
                  </a>
                </DropdownMenuItem>
              </DropdownMenuGroup>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="container py-6">
      <slot />
    </main>
  </div>
</template>

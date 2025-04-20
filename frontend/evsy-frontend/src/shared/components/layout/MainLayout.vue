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
          <nav class="flex items-center space-x-6 text-sm font-medium">
            <NavigationMenu>
              <NavigationMenuList>
                <NavigationMenuItem>
                  <NavigationMenuTrigger>Events</NavigationMenuTrigger>
                  <NavigationMenuContent>
                    <ul class="grid gap-3 p-4 md:w-[400px] lg:w-[500px]">
                      <li>
                        <NavigationMenuLink as-child>
                          <RouterLink to="/events">
                            <div class="text-sm leading-none font-medium">All Events</div>
                            <p class="text-muted-foreground line-clamp-2 text-sm leading-snug">
                              View and manage all analytics events
                            </p>
                          </RouterLink>
                        </NavigationMenuLink>
                      </li>
                      <li>
                        <NavigationMenuLink as-child>
                          <RouterLink to="/events/new">
                            <div class="text-sm leading-none font-medium">New Event</div>
                            <p class="text-muted-foreground line-clamp-2 text-sm leading-snug">
                              Create a new analytics event
                            </p>
                          </RouterLink>
                        </NavigationMenuLink>
                      </li>
                    </ul>
                  </NavigationMenuContent>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <NavigationMenuTrigger>Fields</NavigationMenuTrigger>
                  <NavigationMenuContent>
                    <ul class="grid gap-3 p-4 md:w-[400px] lg:w-[500px]">
                      <li>
                        <NavigationMenuLink as-child>
                          <RouterLink to="/fields">
                            <div class="text-sm leading-none font-medium">All Fields</div>
                            <p class="text-muted-foreground line-clamp-2 text-sm leading-snug">
                              View and manage event properties
                            </p>
                          </RouterLink>
                        </NavigationMenuLink>
                      </li>
                      <li>
                        <NavigationMenuLink as-child>
                          <RouterLink to="/fields/new">
                            <div class="text-sm leading-none font-medium">New Field</div>
                            <p class="text-muted-foreground line-clamp-2 text-sm leading-snug">
                              Create a new event property
                            </p>
                          </RouterLink>
                        </NavigationMenuLink>
                      </li>
                    </ul>
                  </NavigationMenuContent>
                </NavigationMenuItem>
                <NavigationMenuItem>
                  <NavigationMenuTrigger>Tags</NavigationMenuTrigger>
                  <NavigationMenuContent>
                    <ul class="grid gap-3 p-4 md:w-[400px] lg:w-[500px]">
                      <li>
                        <NavigationMenuLink as-child>
                          <RouterLink to="/tags">
                            <div class="text-sm leading-none font-medium">All Tags</div>
                            <p class="text-muted-foreground line-clamp-2 text-sm leading-snug">
                              View and manage event tags
                            </p>
                          </RouterLink>
                        </NavigationMenuLink>
                      </li>
                      <li>
                        <NavigationMenuLink as-child>
                          <RouterLink to="/tags/new">
                            <div class="text-sm leading-none font-medium">New Tag</div>
                            <p class="text-muted-foreground line-clamp-2 text-sm leading-snug">
                              Create a new event tag
                            </p>
                          </RouterLink>
                        </NavigationMenuLink>
                      </li>
                    </ul>
                  </NavigationMenuContent>
                </NavigationMenuItem>
              </NavigationMenuList>
            </NavigationMenu>
          </nav>
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

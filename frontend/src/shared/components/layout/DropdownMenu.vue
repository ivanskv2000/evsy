<script setup lang="ts">
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

import { ref } from 'vue'
import ThemeProvider from '@/shared/components/providers/theme-provider.vue'

const isDropdownOpen = ref(false)
</script>

<template>
  <ThemeProvider v-slot="{ toggleTheme }">
  <DropdownMenu v-model:open="isDropdownOpen">
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
          <DropdownMenuItem
            @click="
              () => {
                toggleTheme()
              }
            "
            @select.prevent
            class="relative flex items-center justify-start"
          >
            <span class="relative mr-2 h-4 w-4">
              <Icon
                icon="radix-icons:moon"
                class="absolute inset-0 scale-100 opacity-100 dark:scale-0 dark:opacity-0"
              />
              <Icon
                icon="radix-icons:sun"
                class="absolute inset-0 scale-0 opacity-0 dark:scale-100 dark:opacity-100"
              />
            </span>
            <span>Toggle theme</span>
          </DropdownMenuItem>
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
</ThemeProvider>
</template>

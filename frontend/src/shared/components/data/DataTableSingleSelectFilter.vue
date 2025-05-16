<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { computed } from 'vue'
import { cn } from '@/shared/utils/general'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

import { Popover, PopoverTrigger, PopoverContent } from '@/shared/ui/popover'
import {
  Command,
  CommandInput,
  CommandList,
  CommandItem,
  CommandGroup,
  CommandEmpty,
} from '@/shared/ui/command'

interface Props {
  column?: Column<TData, TValue>
  title?: string
  placeholder?: string
  icon?: string
  options: string[]
  disabled?: boolean
}

const props = defineProps<Props>()
const selectedValue = computed(() => props.column?.getFilterValue() as string | undefined)
</script>

<template>
  <div class="flex items-center gap-1">
    <Popover>
      <PopoverTrigger as-child>
        <Button
          :disabled="disabled"
          variant="outline"
          :class="{
            'justify-between border-dashed': true,
            'w-[18ch]': selectedValue,
          }"
          :title="selectedValue"
        >
          <div class="flex items-center truncate">
            <Icon :icon="icon || 'radix-icons:plus-circled'" :class="cn('mr-2 h-4 w-4')" />
            {{ title }}
            <div v-if="selectedValue" class="text-muted-foreground ml-2 truncate">
              / {{ selectedValue }}
            </div>
          </div>
        </Button>
      </PopoverTrigger>

      <PopoverContent class="w-[200px] p-0" align="start">
        <Command>
          <CommandInput :placeholder="placeholder" />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup>
              <CommandItem
                v-for="option in options"
                :key="option"
                :value="option"
                @select="() => column?.setFilterValue(option)"
              >
                {{ option }}
              </CommandItem>
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>

    <Button
      v-if="selectedValue"
      variant="ghost"
      size="icon"
      class="text-muted-foreground hover:text-destructive h-8 w-8 shrink-0"
      @click="column?.setFilterValue(undefined)"
    >
      <Icon icon="radix-icons:cross-2" class="h-4 w-4" />
      <span class="sr-only">Clear filter</span>
    </Button>
  </div>
</template>

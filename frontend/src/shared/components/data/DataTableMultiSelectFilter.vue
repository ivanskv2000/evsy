<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { cn } from '@/shared/utils/general'
import { Badge } from '@/shared/ui/badge'
import { Button } from '@/shared/ui/button'

import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from '@/shared/ui/command'
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/ui/popover'
import { Separator } from '@/shared/ui/separator'

import { computed } from 'vue'
import { Icon } from '@iconify/vue'

interface DataTableFacetedFilter {
  column?: Column<TData, TValue>
  title?: string
  icon?: string
  options: string[]
}

const props = defineProps<DataTableFacetedFilter>()

const facets = computed(() => props.column?.getFacetedUniqueValues())
const selectedValues = computed(() => new Set(props.column?.getFilterValue() as string[]))
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button variant="outline" class="border-dashed">
        <div class="flex items-center truncate">
          <Icon :icon="icon || 'radix-icons:plus-circled'" :class="cn('mr-2 h-4 w-4')" />
          {{ title }}
        </div>
        <template v-if="selectedValues.size > 0">
          <Separator orientation="vertical" class="mx-2 h-4" />
          <Badge variant="secondary" class="rounded-sm px-1 font-normal lg:hidden">
            {{ selectedValues.size }}
          </Badge>
          <div class="hidden space-x-1 lg:flex">
            <Badge
              v-if="selectedValues.size > 2"
              variant="secondary"
              class="rounded-sm px-1 font-normal"
            >
              {{ selectedValues.size }} selected
            </Badge>

            <template v-else>
              <Badge
                v-for="option in options.filter(option => selectedValues.has(option))"
                :key="option"
                variant="secondary"
                class="rounded-sm px-1 font-normal"
              >
                {{ option }}
              </Badge>
            </template>
          </div>
        </template>
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[200px] p-0" align="start">
      <Command>
        <CommandInput :placeholder="title" />
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>
          <CommandGroup>
            <CommandItem
              v-for="option in options"
              :key="option"
              :value="option"
              @select="
                () => {
                  const isSelected = selectedValues.has(option)
                  if (isSelected) {
                    selectedValues.delete(option)
                  } else {
                    selectedValues.add(option)
                  }
                  const filterValues = Array.from(selectedValues)
                  column?.setFilterValue(filterValues.length ? filterValues : undefined)
                }
              "
            >
              <div
                :class="
                  cn(
                    'border-primary mr-2 flex h-4 w-4 items-center justify-center rounded-sm border',
                    selectedValues.has(option)
                      ? 'bg-primary text-primary-foreground'
                      : 'opacity-50 [&_svg]:invisible'
                  )
                "
              >
                <Icon icon="radix-icons:check" :class="cn('text-background h-4 w-4')" />
              </div>
              <span class="truncate">{{ option }}</span>
              <span
                v-if="facets?.get(option)"
                class="ml-auto flex h-4 w-4 items-center justify-center font-mono text-xs"
              >
                {{ facets.get(option) }}
              </span>
              <span
                v-else
                class="ml-auto flex h-4 w-4 items-center justify-center font-mono text-xs"
              >
                0
              </span>
            </CommandItem>
          </CommandGroup>

          <template v-if="selectedValues.size > 0">
            <CommandSeparator />
            <CommandGroup>
              <CommandItem
                :value="{ label: 'Clear filters' }"
                class="text-destructive justify-center text-center"
                @select="column?.setFilterValue(undefined)"
              >
                Clear filters
              </CommandItem>
            </CommandGroup>
          </template>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>

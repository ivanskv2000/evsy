<script setup lang="ts" generic="TData, TValue">
import type { Column } from '@tanstack/vue-table'
import { Icon } from '@iconify/vue'

import { cn } from '@/shared/utils/general'
import { Button } from '@/shared/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/shared/ui/dropdown-menu'

interface DataTableColumnHeaderProps {
  column: Column<TData, TValue>
  title: string
  align?: 'left' | 'center' | 'right'
}

defineProps<DataTableColumnHeaderProps>()
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<template>
  <div
    v-if="column.getCanSort()"
    :class="
      cn(
        {
          'text-left': align === 'left',
          'text-center': align === 'center',
          'text-right': align === 'right',
        },
        $attrs.class ?? ''
      )
    "
  >
    <DropdownMenu>
      <DropdownMenuTrigger as-child>
        <Button
          variant="ghost"
          size="sm"
          :class="{
            'data-[state=open]:bg-accent h-8': true,
            '-ml-3': align !== 'center',
          }"
        >
          <span>{{ title }}</span>
          <Icon
            icon="radix-icons:arrow-down"
            v-if="column.getIsSorted() === 'desc'"
            class="ml-2 h-4 w-4"
          />
          <Icon
            icon="radix-icons:arrow-up"
            v-else-if="column.getIsSorted() === 'asc'"
            class="ml-2 h-4 w-4"
          />
          <Icon icon="radix-icons:caret-sort" v-else class="ml-2 h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="start">
        <DropdownMenuItem @click="column.toggleSorting(false)">
          <Icon icon="radix-icons:arrow-up" class="text-muted-foreground/70 mr-2 h-3.5 w-3.5" />
          Asc
        </DropdownMenuItem>

        <DropdownMenuItem @click="column.toggleSorting(true)">
          <Icon icon="radix-icons:arrow-down" class="text-muted-foreground/70 mr-2 h-3.5 w-3.5" />
          Desc
        </DropdownMenuItem>

        <div v-if="column.getCanHide()">
          <DropdownMenuSeparator />
          <DropdownMenuItem @click="column.toggleVisibility(false)">
            <Icon icon="radix-icons:eye-none" class="text-muted-foreground/70 mr-2 h-3.5 w-3.5" />
            Hide
          </DropdownMenuItem>
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  </div>

  <div v-else :class="$attrs.class">
    {{ title }}
  </div>
</template>

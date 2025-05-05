<script setup lang="ts" generic="TData">
import { type Table } from '@tanstack/vue-table'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/ui/button'

defineProps<{
  table: Table<TData>
}>()
</script>

<template>
  <div class="flex items-center justify-center gap-2 px-2">
    <Button
      variant="ghost"
      size="sm"
      :disabled="!table.getCanPreviousPage()"
      @click="table.previousPage()"
    >
      <span class="sr-only">Previous page</span>
      <Icon icon="radix-icons:chevron-left" class="h-4 w-4" />
    </Button>

    <span class="text-muted-foreground text-sm">
      Page {{ table.getState().pagination.pageIndex + 1 }} of {{ table.getPageCount() }}
    </span>

    <Button variant="ghost" size="sm" :disabled="!table.getCanNextPage()" @click="table.nextPage()">
      <span class="sr-only">Next page</span>
      <Icon icon="radix-icons:chevron-right" class="h-4 w-4" />
    </Button>
  </div>
</template>

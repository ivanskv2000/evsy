<script setup lang="ts" generic="TData">
import type { Table } from '@tanstack/vue-table'
import {
  Table as TableComponent,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/shared/ui/table'
import { Icon } from '@iconify/vue'

import { FlexRender } from '@tanstack/vue-table'

defineProps<{
  table: Table<TData>,
  isLoading?: boolean
}>()
</script>
<template>
  <div class="rounded-md border">
    <TableComponent>
      <TableHeader>
        <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
          <TableHead v-for="header in headerGroup.headers" :key="header.id">
            <FlexRender
              v-if="!header.isPlaceholder"
              :render="header.column.columnDef.header"
              :props="header.getContext()"
            />
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <template v-if="table.getRowModel().rows?.length">
          <TableRow
            v-for="row in table.getRowModel().rows"
            :key="row.id"
            :data-state="row.getIsSelected() ? 'selected' : undefined"
          >
            <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
              <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
            </TableCell>
          </TableRow>
        </template>

        <template v-else-if="isLoading">
          <TableRow>
            <TableCell :colspan="table.getVisibleFlatColumns().length" class="h-24 text-center">
              <div>
              <Icon icon="radix-icons:reload" class="inline animate-spin h-4 w-4 text-foreground" />
            </div>
            </TableCell>
          </TableRow>
        </template>

        <template v-else>
          <TableRow>
            <TableCell :colspan="table.getVisibleFlatColumns().length" class="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        </template>
      </TableBody>
    </TableComponent>
  </div>
</template>

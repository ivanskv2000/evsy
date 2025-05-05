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

import { FlexRender } from '@tanstack/vue-table'

defineProps<{
  table: Table<TData>
}>()
</script>

<template>
  <Transition name="fade" appear>
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

            <TableRow
              v-for="n in table.getState().pagination.pageSize - table.getRowModel().rows.length"
              :key="'placeholder-' + n"
              class="pointer-events-none border-transparent opacity-0"
              aria-hidden="true"
            >
              <TableCell v-for="column in table.getVisibleFlatColumns()" :key="column.id">
                <slot name="row-placeholder"> &nbsp; </slot>
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
  </Transition>
</template>

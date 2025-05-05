import { h } from 'vue'
import type { Field } from '@/modules/fields/types.ts'
import type { ColumnDef } from '@tanstack/vue-table'
import { RouterLink } from 'vue-router'
import DataTableColumnHeader from '@/shared/components/data/DataTableColumnHeader.vue'

export function getEventFieldsColumns(): ColumnDef<Field>[] {
  return [
    {
      accessorKey: 'id',
      enableHiding: false,
      header: ({ column }) =>
        h(DataTableColumnHeader<Field, unknown>, {
          column,
          title: 'ID',
          align: 'center',
        }),
      cell: ({ row }) => {
        const id = Number.parseInt(row.getValue('id'))
        return h('div', { class: 'text-center font-medium' }, id)
      },
    },
    {
      accessorKey: 'name',
      enableHiding: false,
      header: ({ column }) =>
        h(DataTableColumnHeader<Field, unknown>, {
          column,
          title: 'Name',
        }),
      cell: ({ row }) => {
        const name = String(row.getValue('name'))
        const id = Number.parseInt(row.getValue('id'))
        return h(
          'div',
          { class: 'text-left font-medium' },
          h(RouterLink, { to: `/fields/${id}` }, { default: () => name })
        )
      },
    },
    {
      accessorKey: 'field_type',
      enableHiding: false,
      header: ({ column }) =>
        h(DataTableColumnHeader<Field, unknown>, {
          column,
          title: 'Type',
        }),
      cell: ({ row }) => {
        const field_type = String(row.getValue('field_type'))
        return h('div', { class: 'text-left font-medium' }, field_type)
      },
      filterFn: 'equals',
    },
    {
      accessorKey: 'description',
      enableHiding: false,
      enableSorting: false,
      header: ({ column }) =>
        h(DataTableColumnHeader<Field, unknown>, {
          column,
          title: 'Description',
        }),
      cell: ({ row }) => {
        const description = String(row.getValue('description'))

        return h(
          'div',
          {
            class: 'max-w-[300px] truncate whitespace-nowrap overflow-hidden text-muted-foreground',
            title: description,
            style: {
              userSelect: 'text',
              cursor: 'text',
            },
          },
          description
        )
      },
    },
  ]
}

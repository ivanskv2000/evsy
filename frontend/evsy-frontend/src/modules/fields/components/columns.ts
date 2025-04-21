import { h } from 'vue'
import type { Field } from '@/modules/fields/types.ts'
import type { ColumnDef } from '@tanstack/vue-table'
import DropdownAction from '@/shared/components/data/DataTableDropdown.vue'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/components/ui/button'
import { RouterLink } from 'vue-router'

export const columns: ColumnDef<Field>[] = [
  {
    accessorKey: 'id',
    header: () => h('div', { class: 'text-center' }, 'ID'),
    cell: ({ row }) => {
      const id = Number.parseInt(row.getValue('id'))
      return h('div', { class: 'text-center font-medium' }, id)
    },
  },
  {
    accessorKey: 'name',
    header: ({ column }) => {
      return h(
        Button,
        {
          variant: 'ghost',
          onClick: () => {
            const currentSort = column.getIsSorted()
            if (currentSort === 'asc') {
              column.toggleSorting(true)
            } else if (currentSort === 'desc') {
              column.clearSorting()
            } else {
              column.toggleSorting(false)
            }
          },
        },
        () => [
          'Name',
          h(Icon, {
            icon: column.getIsSorted()
              ? column.getIsSorted() === 'asc'
                ? 'radix-icons:caret-up'
                : 'radix-icons:caret-down'
              : 'radix-icons:caret-sort',
            class: 'ml-2 h-4 w-4',
          }),
        ]
      )
    },
    cell: ({ row }) => {
      const name = String(row.getValue('name'))
      const id = Number.parseInt(row.getValue('id'))
      return h(
        'div',
        { class: 'text-left font-medium' },
        h(RouterLink, { to: `/fields/${id}` }, name)
      )
    },
  },
  {
    accessorKey: 'field_type',
    header: () => h('div', { class: 'text-left' }, 'Type'),
    cell: ({ row }) => {
      const field_type = String(row.getValue('field_type'))
      return h('div', { class: 'text-left font-medium' }, field_type)
    },
    filterFn: 'equals',
  },
  {
    id: 'actions',
    enableHiding: false,
    cell: ({ row }) => {
      const field = row.original

      return h(
        'div',
        { class: 'relative' },
        h(DropdownAction, {
          field,
        })
      )
    },
  },
]

import { h } from 'vue'
import type { Event } from '@/modules/events/types.ts'
import type { ColumnDef } from '@tanstack/vue-table'
import EventsDataTableDropdown from '@/modules/events/components/EventsDataTableDropdown.vue'
import { RouterLink } from 'vue-router'
import DataTableColumnHeader from '@/shared/components/data/DataTableColumnHeader.vue'
import { Badge } from '@/shared/ui/badge'

export function getEventColumns(
  onEdit: (event: Event) => void,
  onDelete: (event: Event) => void
): ColumnDef<Event>[] {
  return [
    {
      accessorKey: 'id',
      enableHiding: false,
      header: ({ column }) =>
        h(DataTableColumnHeader<Event, unknown>, {
          column: column,
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
        h(DataTableColumnHeader<Event, unknown>, {
          column: column,
          title: 'Name',
        }),
      cell: ({ row }) => {
        const name = String(row.getValue('name'))
        const id = Number.parseInt(row.getValue('id'))
        return h(
          'div',
          { class: 'text-left font-medium' },
          h(RouterLink, { to: `/events/${id}` }, { default: () => name })
        )
      },
    },
    {
      accessorKey: 'tags',
      enableHiding: false,
      enableSorting: false,
      header: ({ column }) =>
        h(DataTableColumnHeader<Event, unknown>, {
          column: column,
          title: 'Tags',
        }),
      cell: ({ row }) => {
        const event = row.original
        const tags = event.tags
        return h(
          'div',
          {
            class:
              'flex flex-row gap-1 text-left font-medium max-w-40 overflow-auto hide-scrollbar scroll-x-bounce',
            ref: 'scrollContainer',
          },
          tags.map(tag => h(Badge, { variant: 'outline' }, { default: () => tag.id }))
        )
      },
    },
    {
      id: 'actions',
      enableHiding: false,
      enableSorting: false,
      cell: ({ row }) => {
        const event = row.original

        return h(
          'div',
          { class: 'relative' },
          h(EventsDataTableDropdown, {
            event,
            onEditMe: () => onEdit(event),
            onDeleteMe: () => onDelete(event),
          })
        )
      },
    },
  ]
}

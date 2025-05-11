import { h } from 'vue'
import type { Event } from '@/modules/events/types.ts'
import type { Tag } from '@/modules/tags/types.ts'
import type { ColumnDef } from '@tanstack/vue-table'
import EventsDataTableDropdown from '@/modules/events/components/EventsDataTableDropdown.vue'
import { RouterLink } from 'vue-router'
import DataTableColumnHeader from '@/shared/components/data/DataTableColumnHeader.vue'
import { Badge } from '@/shared/ui/badge'
import TagScrollArea from '@/modules/tags/components/TagScrollArea.vue'

export function getEventColumns(
  onEdit: (event: Event) => void,
  onDelete: (event: Event) => void
): ColumnDef<Event>[] {
  return [
    {
      accessorKey: 'id',
      enableHiding: false,
      meta: {
        class: 'w-[6ch] text-center',
        headerClass: 'w-[6ch] text-center',
      },
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
      meta: {
        class: 'w-[18ch]',
        headerClass: 'w-[18ch]',
      },
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
          {
            class: 'truncate whitespace-nowrap overflow-hidden text-left font-medium',
            title: name,
            style: {
              userSelect: 'text',
              cursor: 'text',
            },
          },
          h(RouterLink, { to: `/events/${id}` }, { default: () => name })
        )
      },
    },
    {
      accessorKey: 'description',
      enableSorting: false,
      meta: {
        class: 'w-[22ch]',
        headerClass: 'w-[22ch]',
      },
      header: ({ column }) =>
        h(DataTableColumnHeader<Event, unknown>, {
          column,
          title: 'Description',
        }),
      cell: ({ row }) => {
        const description = String(row.getValue('description') ?? '-')

        return h(
          'div',
          {
            class: 'truncate whitespace-nowrap overflow-hidden text-muted-foreground',
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
    {
      accessorKey: 'tags',
      enableHiding: false,
      enableSorting: false,
      meta: {
        class: 'w-[18ch]',
        headerClass: 'w-[18ch]',
      },
      header: ({ column }) =>
        h(DataTableColumnHeader<Event, unknown>, {
          column: column,
          title: 'Tags',
        }),
      cell: ({ row }) => {
        const event = row.original
        const tags = event.tags
        return h(
          TagScrollArea,
          {
            class: 'w-[18ch] -ml-4',
            ref: 'scrollContainer',
          },
          () => tags.map(tag => h(Badge, { variant: 'outline' }, { default: () => tag.id }))
        )
      },
      filterFn: (row, id, value) => {
        const tags = row.getValue(id) as Tag[]
        return tags.some(tag => tag.id === value)
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

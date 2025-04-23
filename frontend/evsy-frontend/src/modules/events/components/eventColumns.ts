import { h } from 'vue'
import type { Event } from '@/modules/events/types.ts'
import type { ColumnDef } from '@tanstack/vue-table'
import EventsDataTableDropdown from '@/modules/events/components/EventsDataTableDropdown.vue'
import { RouterLink } from 'vue-router'
import DataTableColumnHeader from '@/shared/components/data/DataTableColumnHeader.vue'

export function getEventColumns(
  onUpdated: (event: Event) => void,
  onDeleted: (id: number) => void
): ColumnDef<Event>[] {
  return [
    {
      accessorKey: 'id',
      enableHiding: false,
      header: ({ column }) =>
        h(DataTableColumnHeader, {
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
        h(DataTableColumnHeader, {
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
            handleUpdateRow: (updatedEvent: Event) => onUpdated(updatedEvent),
            handleDeleteRow: () => onDeleted(event.id),
          })
        )
      },
    },
  ]
}

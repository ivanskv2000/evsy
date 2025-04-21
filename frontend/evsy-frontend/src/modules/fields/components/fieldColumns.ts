import { h } from 'vue'
import type { Field } from '@/modules/fields/types.ts'
import type { ColumnDef } from '@tanstack/vue-table'
import DataTableDropdown from '@/shared/components/data/DataTableDropdown.vue'
import { RouterLink } from 'vue-router'
import DataTableColumnHeader from '@/shared/components/data/DataTableColumnHeader.vue'

export function getFieldColumns(
  onUpdated: (field: Field) => void,
  onDeleted: (id: number) => void
): ColumnDef<Field>[] {
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
          h(RouterLink, { to: `/fields/${id}` }, name)
        )
      },
    },
    {
      accessorKey: 'field_type',
      header: ({ column }) =>
        h(DataTableColumnHeader, {
          column: column,
          title: 'Type',
        }),
      cell: ({ row }) => {
        const field_type = String(row.getValue('field_type'))
        return h('div', { class: 'text-left font-medium' }, field_type)
      },
      filterFn: 'equals',
    },
    {
      id: 'actions',
      enableHiding: false,
      enableSorting: false,
      cell: ({ row }) => {
        const field = row.original

        return h(
          'div',
          { class: 'relative' },
          h(DataTableDropdown, {
            field,
            handleUpdateRow: (updatedField: Field) => onUpdated(updatedField),
            handleDeleteRow: () => onDeleted(field.id),
          })
        )
      },
    },
  ]
}

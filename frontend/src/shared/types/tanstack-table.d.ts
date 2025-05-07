import '@tanstack/vue-table'

declare module '@tanstack/vue-table' {
  interface ColumnMeta {
    class?: string
    headerClass?: string
  }
}

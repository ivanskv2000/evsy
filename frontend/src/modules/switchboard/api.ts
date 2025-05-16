import { api } from '@/shared/utils/api'
import type { ExportBundle, ImportBundle, ResetPreview } from './types'

export const seedDatabase = () => api.post('/admin/seed')

export const resetDatabase = (dryRun = false) =>
  api
    .post<ResetPreview | { status: string }>('/admin/reset', null, {
      params: { dry_run: dryRun },
    })
    .then(r => r.data)

export const importData = (payload: ImportBundle, source = 'json') =>
  api.post('/admin/io/import', payload, { params: { source } })

export const exportData = (target = 'json') =>
  api.get<ExportBundle>('/admin/io/export', { params: { target } })

import type { Field } from './types'
import { createCrudApi } from '@/shared/api/crudApiFactory'

export const fieldApi = createCrudApi<Field>('fields')

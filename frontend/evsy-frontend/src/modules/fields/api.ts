import type { Field } from './types'
import { createCrudApi } from '@/shared/api/crudApiFactory'
import type { FieldFormValues } from './validation/fieldSchema'

export const fieldApi = createCrudApi<Field, FieldFormValues>('fields')

import type { Tag } from './types'
import { createCrudApi } from '@/shared/api/crudApiFactory'
import type { TagFormValues } from './validation/tagSchema'

export const tagApi = createCrudApi<Tag, TagFormValues>('tags')

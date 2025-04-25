import type { Tag } from './types'
import { createCrudApi } from '@/shared/api/crudApiFactory'

export const tagApi = createCrudApi<Tag>('tags')

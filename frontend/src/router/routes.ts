import { fieldsRoutes } from '@/modules/fields/router'
import { eventsRoutes } from '@/modules/events/router'
import { tagsRoutes } from '@/modules/tags/router'
import { switchboardRoutes } from '@/modules/switchboard/router'
import { authRoutes } from '@/modules/auth/router'

export const routes = [
  { path: '/', redirect: '/events' },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/shared/pages/NotFoundPage.vue'),
  },
  ...eventsRoutes,
  ...fieldsRoutes,
  ...tagsRoutes,
  ...switchboardRoutes,
  ...authRoutes,
]

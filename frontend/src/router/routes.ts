import { fieldsRoutes } from '@/modules/fields/router'
import { eventsRoutes } from '@/modules/events/router'
import { tagsRoutes } from '@/modules/tags/router'
import { switchboardRoutes } from '@/modules/switchboard/router'
import { authRoutes } from '@/modules/auth/router'
import { userRoutes } from '@/modules/user/router'
import OAuthCallback from '@/modules/auth/oauth/OAuthCallback.vue'

export const routes = [
  { path: '/', redirect: '/events' },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/shared/pages/NotFoundPage.vue'),
  },
  {
    path: '/oauth/callback',
    component: OAuthCallback,
  },
  ...eventsRoutes,
  ...fieldsRoutes,
  ...tagsRoutes,
  ...switchboardRoutes,
  ...authRoutes,
  ...userRoutes,
]

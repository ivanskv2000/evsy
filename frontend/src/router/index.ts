import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { routes } from './routes'

const publicPages = ['/login', '/signup', '/landing', '/oauth/callback']

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

router.beforeEach((to, _from, next) => {
  const auth = useAuthStore()
  const isPublic = publicPages.includes(to.path)

  if (!isPublic && !auth.token) {
    next({ path: '/login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router

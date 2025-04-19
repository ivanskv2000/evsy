import type { RouteRecordRaw } from 'vue-router'
import TagsPage from './pages/TagsPage.vue'

export const tagsRoutes: RouteRecordRaw[] = [
  { 
    path: '/tags', 
    name: 'Tags', 
    component: TagsPage 
  },
  { 
    path: '/tags/new', 
    name: 'NewTag', 
    component: TagsPage 
  },
] 
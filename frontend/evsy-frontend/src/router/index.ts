import { createRouter, createWebHistory } from 'vue-router'
import FieldsPage from '@/pages/FieldsPage.vue'
import EventsPage from '@/pages/EventsPage.vue'
import TagsPage from '@/pages/TagsPage.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/events' },
    { path: '/events', name: 'Events', component: EventsPage },
    { path: '/events/new', name: 'NewEvent', component: EventsPage },
    { path: '/fields', name: 'Fields', component: FieldsPage },
    { path: '/fields/new', name: 'NewField', component: FieldsPage },
    { path: '/tags', name: 'Tags', component: TagsPage },
    { path: '/tags/new', name: 'NewTag', component: TagsPage }
  ]
})
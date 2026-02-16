import type { App } from 'vue'
import { VueQueryPlugin, type VueQueryPluginOptions, QueryClient } from '@tanstack/vue-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
    },
  },
})

const vueQueryPluginOptions: VueQueryPluginOptions = {
  queryClient,
}

export const installVueQuery = (app: App) => {
  app.use(VueQueryPlugin, vueQueryPluginOptions)
}

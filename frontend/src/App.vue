<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import MainLayout from '@/shared/components/layout/MainLayout.vue'
import { Toaster } from '@/shared/ui/sonner'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import router from './router'
import { VueQueryDevtools } from '@tanstack/vue-query-devtools'
import { useEnhancedToast } from './shared/composables/useEnhancedToast'
import { queryClient } from './shared/plugins/vue-query'

const auth = useAuthStore()
const route = useRoute()
const { showError } = useEnhancedToast()

const globalErrorHandler = (error: unknown) => {
  if (error && typeof error === 'object' && 'silent' in error && error.silent) return
  showError(error)
}

const queryCache = queryClient.getQueryCache()
const mutationCache = queryClient.getMutationCache()
queryCache.config.onError = globalErrorHandler
mutationCache.config.onError = globalErrorHandler

if (auth.token) {
  auth.fetchCurrentUser().catch(() => {
    auth.logout()
  })
}

window.addEventListener('message', async event => {
  const { token, redirect } = event.data
  if (token) {
    auth.token = token
    await auth.fetchCurrentUser()
    router.replace(redirect || '/events')
  }
})
</script>

<template>
  <Toaster richColors />

  <MainLayout>
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in" appear>
        <component :is="Component" :key="route.fullPath" />
      </Transition>
    </RouterView>
  </MainLayout>

  <VueQueryDevtools />
</template>

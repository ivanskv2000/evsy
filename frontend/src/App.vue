<script setup lang="ts">
import { RouterView } from 'vue-router'
import MainLayout from '@/shared/components/layout/MainLayout.vue'
import { Toaster } from '@/shared/ui/sonner'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import router from './router'

const auth = useAuthStore()

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
        <component :is="Component" />
      </Transition>
    </RouterView>
  </MainLayout>
</template>

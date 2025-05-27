<script setup lang="ts">
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { api } from '@/shared/utils/api'

const route = useRoute()
const { showError } = useEnhancedToast()

onMounted(async () => {
  const code = route.query.code as string | undefined
  const provider = route.query.provider as 'google' | 'github' | undefined
  const state = route.query.state
    ? decodeURIComponent(atob(route.query.state as string))
    : '/events'

  if (!code || !provider) {
    showError('OAuth login failed.')
    window.close()
    return
  }

  try {
    const response = await api.post('/auth/oauth', {
      provider,
      token: code,
    })
    const accessToken = response.data.access_token

    window.opener?.postMessage({ token: accessToken, redirect: state }, window.origin)
    window.close()
  } catch {
    showError('OAuth login failed.')
    window.close()
  }
})
</script>

<template>
  <div class="p-4 text-center">
    <p class="text-muted-foreground text-sm">Finalizing login...</p>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { onMounted } from 'vue'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { api } from '@/shared/utils/api'

const route = useRoute()
const { showError } = useEnhancedToast()

function isSafeRedirect(path: string | undefined): path is string {
  return !!path && path.startsWith('/') && !path.startsWith('//')
}

onMounted(async () => {
  const code = route.query.code as string | undefined
  const stateRaw = route.query.state as string | undefined

  let provider: 'google' | 'github' | undefined
  let redirect = '/events'

  if (stateRaw) {
    try {
      const decoded = JSON.parse(atob(stateRaw))
      provider = decoded.provider
      if (isSafeRedirect(decoded.redirect)) {
        redirect = decoded.redirect
      }
    } catch {
      provider = undefined
      redirect = '/events'
    }
  }

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

    window.opener?.postMessage({ token: accessToken, redirect }, window.origin)
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

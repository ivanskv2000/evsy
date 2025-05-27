<script setup lang="ts">
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

const props = defineProps<{ provider: 'google' | 'github' }>()
const { showError } = useEnhancedToast()

function handleOAuth() {
  const width = 500
  const height = 600
  const left = window.screenX + (window.outerWidth - width) / 2
  const top = window.screenY + (window.outerHeight - height) / 2

  const popup = window.open(
    `${import.meta.env.VITE_API_URL}/auth/oauth/init/${props.provider}`,
    'oauth',
    `width=${width},height=${height},top=${top},left=${left}`
  )

  if (!popup) {
    showError('Popup blocked. Please allow popups and try again.')
  }
}
</script>

<template>
  <Button variant="outline" class="w-full" @click="handleOAuth">
    <Icon :icon="props.provider === 'google' ? 'mdi:google' : 'mdi:github'" class="mr-2 h-4 w-4" />
    Sign in with {{ props.provider === 'google' ? 'Google' : 'GitHub' }}
  </Button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

const router = useRouter()
const auth = useAuthStore()

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <Button v-if="auth.token" variant="ghost" class="text-sm" @click="handleLogout">
    <Icon icon="radix-icons:exit" class="mr-2 h-4 w-4" />
    Log out
  </Button>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { Button } from '@/shared/ui/button'
import { Icon } from '@iconify/vue'

const auth = useAuthStore()
</script>

<template>
  <Button v-if="!auth.token" variant="ghost" class="text-sm" as-child>
    <RouterLink to="/login">
      <Icon icon="radix-icons:enter" class="mr-2 h-4 w-4" />
      Log in
    </RouterLink>
  </Button>
</template>

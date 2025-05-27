<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Button } from '@/shared/ui/button'
import { Input } from '@/shared/ui/input'
import { Label } from '@/shared/ui/label'
import OauthButton from '@/modules/auth/oauth/OauthButton.vue'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const { run: runSignup, isLoading } = useAsyncTask()
const { showSuccess } = useEnhancedToast()

const handleSubmit = () => {
  runSignup(
    () =>
      auth.signup(email.value, password.value).then(() => auth.login(email.value, password.value)),
    () => {
      showSuccess('Account created successfully! You are now logged in.')
      router.push('/events')
    }
  )
}
</script>

<template>
  <form class="grid gap-4" @submit.prevent="handleSubmit">
    <div class="grid gap-2">
      <Label for="email">Email</Label>
      <Input id="email" v-model="email" type="email" placeholder="name@example.com" required />
    </div>
    <div class="grid gap-2">
      <Label for="password">Password</Label>
      <Input id="password" v-model="password" type="password" required />
    </div>
    <Button type="submit" class="w-full" :disabled="isLoading">
      {{ isLoading ? 'Creating...' : 'Create an account' }}
    </Button>
    <div class="flex gap-2">
      <OauthButton class="flex-1" provider="github" />
      <OauthButton class="flex-1" provider="google" />
    </div>
  </form>
  <div class="mt-4 text-center text-sm">
    Already have an account?
    <RouterLink to="/login" class="underline underline-offset-4"> Sign in </RouterLink>
  </div>
</template>

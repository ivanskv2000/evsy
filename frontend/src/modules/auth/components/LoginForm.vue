<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { Button } from '@/shared/ui/button'
import { Input } from '@/shared/ui/input'
import { Label } from '@/shared/ui/label'
import { Icon } from '@iconify/vue'
import { useRouter, useRoute } from 'vue-router'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const redirect = route.query.redirect as string | undefined

const { run: runLogin, isLoading } = useAsyncTask()
const { showSuccess } = useEnhancedToast()

const handleSubmit = () => {
  runLogin(
    () => auth.login(email.value, password.value),
    () => {
      showSuccess(`Successfully logged in!`)
      router.push(redirect || '/events')
    }
  )
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="mt-2 space-y-6">
    <div class="grid gap-6">
      <div class="flex flex-col gap-4">
        <Button variant="outline" class="w-full" disabled>
          <Icon icon="simple-icons:google" class="mr-2 h-4 w-4" />
          Login with Google
        </Button>
        <Button variant="outline" class="w-full" disabled>
          <Icon icon="simple-icons:github" class="mr-2 h-4 w-4" />
          Login with GitHub
        </Button>
      </div>
      <div
        class="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t"
      >
        <span class="bg-background text-muted-foreground relative z-10 px-2">
          Or continue with
        </span>
      </div>
      <div class="grid gap-6">
        <div class="grid gap-2">
          <Label html-for="email">Email</Label>
          <Input id="email" v-model="email" type="email" placeholder="m@example.com" required />
        </div>
        <div class="grid gap-2">
          <div class="flex items-center">
            <Label html-for="password">Password</Label>
            <a href="#" class="ml-auto text-sm underline-offset-4 hover:underline">
              Forgot your password?
            </a>
          </div>
          <Input id="password" v-model="password" type="password" required />
        </div>
        <Button type="submit" class="w-full" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </Button>
      </div>
      <div class="text-center text-sm">
        Don't have an account?
        <RouterLink to="/signup" class="underline underline-offset-4"> Sign up </RouterLink>
      </div>
    </div>
  </form>
</template>

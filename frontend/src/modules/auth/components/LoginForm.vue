<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { loginSchema, type LoginFormValues } from '@/modules/auth/validation/loginSchema'

import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/shared/ui/form'
import OauthButton from '@/modules/auth/oauth/OauthButton.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const { showSuccess } = useEnhancedToast()
const { run: runLogin, isLoading } = useAsyncTask()

const redirect = route.query.redirect as string | undefined

const { handleSubmit } = useForm<LoginFormValues>({
  validationSchema: toTypedSchema(loginSchema),
})

const onSubmit = handleSubmit(values => {
  runLogin(
    () => auth.login(values.email, values.password),
    () => {
      showSuccess('Successfully logged in!')
      router.push(redirect || '/events')
    }
  )
})
</script>

<template>
  <form @submit="onSubmit" class="mt-2 space-y-6">
    <div class="grid gap-6">
      <!-- OAuth buttons -->
      <div class="flex flex-col gap-4">
        <OauthButton class="flex-1" provider="github" />
        <OauthButton class="flex-1" provider="google" />
      </div>

      <!-- Divider -->
      <div
        class="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t"
      >
        <span class="bg-background text-muted-foreground relative z-10 px-2">
          Or continue with
        </span>
      </div>

      <!-- Email -->
      <FormField name="email" v-slot="{ componentField }">
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl>
            <Input type="email" placeholder="name@example.com" v-bind="componentField" />
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Password -->
      <FormField name="password" v-slot="{ componentField }">
        <FormItem>
          <FormLabel>Password</FormLabel>
          <FormControl>
            <Input type="password" v-bind="componentField" />
          </FormControl>
          <FormMessage />
        </FormItem>
      </FormField>

      <!-- Submit -->
      <Button type="submit" class="w-full" :disabled="isLoading"> Log In </Button>

      <!-- Link to signup -->
      <div class="text-center text-sm">
        Don’t have an account?
        <RouterLink to="/signup" class="underline underline-offset-4">Sign up</RouterLink>
      </div>
    </div>
  </form>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import { signupSchema, type SignupFormValues } from '@/modules/auth/validation/signupSchema'
import { useAuthStore } from '@/modules/auth/stores/useAuthStore'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

import { Input } from '@/shared/ui/input'
import { Button } from '@/shared/ui/button'
import { FormField, FormItem, FormLabel, FormControl, FormMessage } from '@/shared/ui/form'
import OauthButton from '@/modules/auth/oauth/OauthButton.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const { showSuccess } = useEnhancedToast()
const { run: runSignup, isLoading } = useAsyncTask()

const redirect = route.query.redirect as string | undefined

const { handleSubmit } = useForm<SignupFormValues>({
  validationSchema: toTypedSchema(signupSchema),
})

const onSubmit = handleSubmit(values => {
  runSignup(
    () =>
      auth
        .signup(values.email, values.password)
        .then(() => auth.login(values.email, values.password)),
    () => {
      showSuccess('Account created successfully! You are now logged in.')
      router.push(redirect || '/events')
    }
  )
})
</script>

<template>
  <form @submit="onSubmit" class="mt-2 space-y-6">
    <div class="grid gap-6">
      <!-- OAuth Buttons -->
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
      <Button type="submit" class="w-full" :disabled="isLoading"> Sign Up </Button>

      <!-- Link to login -->
      <div class="text-center text-sm">
        Already have an account?
        <RouterLink :to="{ path: '/login', query: { redirect } }" class="underline underline-offset-4">Log in</RouterLink>
      </div>
    </div>
  </form>
</template>

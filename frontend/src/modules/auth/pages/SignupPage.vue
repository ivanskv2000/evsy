<script setup lang="ts">
import SignupForm from '@/modules/auth/components/SignupForm.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { Card, CardContent } from '@/shared/ui/card'
</script>

<template>
  <div>
    <Header title="Sign Up" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <SignupForm />
      </CardContent>
    </Card>
  </div>
</template>

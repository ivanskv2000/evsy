<script setup lang="ts">
import LoginForm from '@/modules/auth/components/LoginForm.vue'
import Header from '@/shared/components/layout/PageHeader.vue'
import { Card, CardContent } from '@/shared/ui/card'
</script>

<template>
  <div>
    <Header title="Log In" />

    <Card class="mx-auto max-w-md">
      <CardContent>
        <LoginForm />
      </CardContent>
    </Card>
  </div>
</template>

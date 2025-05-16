<script setup lang="ts">
import { Button } from '@/shared/ui/button'
</script>

<template>
  <div class="mt-24 flex flex-col items-center justify-center space-y-4 px-4 text-center">
    <h1 class="text-foreground font-mono text-5xl font-semibold tracking-wide">404</h1>
    <p class="text-muted-foreground max-w-prose text-sm">This page is lost in time.</p>
    <Button variant="link" as-child>
      <RouterLink to="/"> Return to safety </RouterLink>
    </Button>
  </div>
</template>

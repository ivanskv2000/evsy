<script setup lang="ts">
import {
  Card,
  CardContent,
  CardHeader,
  CardDescription,
  CardFooter,
} from '@/shared/ui/card'
import { Skeleton } from '@/shared/ui/skeleton'
</script>

<template>
  <Card>
    <!-- Header -->
    <CardHeader>
      <div class="flex items-center justify-between">
        <!-- Title & Badge -->
        <div class="flex items-center space-x-2">
          <Skeleton class="h-6 w-36 rounded-md" />
          <Skeleton class="h-5 w-16 rounded-full" />
        </div>

        <!-- Action Buttons -->
        <div class="flex space-x-2">
          <Skeleton class="h-8 w-8 rounded" />
          <Skeleton class="h-8 w-8 rounded" />
        </div>
      </div>

      <!-- Description -->
      <CardDescription>
        <Skeleton class="mt-3 h-4 w-60 rounded" />
      </CardDescription>

      <!-- Attributes -->
      <div class="text-muted-foreground mt-4 space-y-3 text-sm">
        <Skeleton class="h-3 w-1/2 rounded" />
        <Skeleton class="h-3 w-2/3 rounded" />
        <Skeleton class="h-3 w-1/3 rounded" />
      </div>
    </CardHeader>

    <!-- Content -->
    <CardContent>
      <Skeleton class="h-16 w-full rounded-md" />
    </CardContent>

    <!-- Footer -->
    <CardFooter>
      <Skeleton class="h-4 w-28 rounded" />
    </CardFooter>
  </Card>
</template>
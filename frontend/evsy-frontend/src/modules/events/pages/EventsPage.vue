<script setup lang="ts">
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/shared/components/ui/card'
import { ref, onMounted } from 'vue'
import { useApiErrorToast, useSuccessToast } from '@/shared/utils/toast'
import { Button } from '@/shared/components/ui/button'

const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <h1 class="flex-1 text-center text-2xl font-bold">Events</h1>
    </div>

    <div class="container mx-auto">
      <!-- TEST ZONE -->
      <Button
        variant="outline"
        @click="
          () => {
            showApiErrorToast()
          }
        "
      >
        Error
      </Button>
      <Button
        variant="outline"
        @click="
          () => {
            showSuccessToast()
          }
        "
      >
        Success
      </Button>
    </div>
  </div>
</template>

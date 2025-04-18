<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card'
import { ref, onMounted } from 'vue'
import { useApiErrorToast } from '@/lib/useApiErrorToast'
import { useSuccessToast } from '@/lib/useSuccessToast'
import { Button } from '@/components/ui/button'


const { showApiErrorToast } = useApiErrorToast()
const { showSuccessToast } = useSuccessToast()
</script>


<template>
  <div>
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-bold text-center flex-1">Events</h1>
    </div>


      <div class="container mx-auto">
            <!-- TEST ZONE -->
            <Button variant="outline" @click="() => {showApiErrorToast()}">
                Error
            </Button>
            <Button variant="outline" @click="() => {showSuccessToast()}">
                Success
            </Button>
      </div>
  </div>
</template> 
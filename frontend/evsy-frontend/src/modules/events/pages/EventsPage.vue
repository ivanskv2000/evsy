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
import Header from '@/shared/components/layout/Header.vue'
</script>

<template>
  <div>
    <Header title="Events" />
    <div class="container mx-auto">
      TBD
    </div>
  </div>
</template>

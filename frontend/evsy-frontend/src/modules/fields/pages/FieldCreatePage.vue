<script setup lang="ts">
import { FieldForm } from '@/modules/fields/components/FieldForm.vue'
import { Button } from '@/shared/components/ui/button'
import { Icon } from '@iconify/vue'
</script>

<template>
    <div>
      <!-- Header with Back button and Title -->
      <div class="mb-6 flex items-center justify-between">
          <Button as-child variant="ghost" class="w-[30px]">
              <RouterLink to="/fields">
                  <Icon icon="radix-icons:caret-left" class="h-4 w-4" />
              </RouterLink>
          </Button>
  
        <h1 class="text-2xl font-bold text-center flex-1">Create new field</h1>
  
        <!-- Пустой элемент для симметрии -->
        <div class="w-[30px]"></div>
      </div>
  
  
      <FieldForm />

      </div>
  </template>

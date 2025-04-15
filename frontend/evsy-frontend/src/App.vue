<script setup lang="ts">
import { RouterView } from 'vue-router'
import MainLayout from '@/components/layout/MainLayout.vue'
</script>

<template>
  <MainLayout>
    <RouterView />
  </MainLayout>
</template>

<style>
@import './index.css';
</style>

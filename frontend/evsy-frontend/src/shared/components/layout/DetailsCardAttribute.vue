<script setup lang="ts">
import { Icon } from '@iconify/vue'

const props = defineProps<{
    icon: string
    label: string
    value?: string
}>()
</script>

<template>
    <div class="flex flex-wrap items-center gap-1">
        <div class="flex items-center gap-1">
            <Icon :icon="icon" class="h-4 w-4" />
            <span>{{ label }}:</span>
        </div>
        <span v-if="value">{{ value }}</span>
        <slot name="value" />
    </div>
</template>
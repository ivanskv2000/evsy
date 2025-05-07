<script setup lang="ts">
import { FieldType } from '@/modules/fields/types'
import { Badge } from '@/shared/ui/badge'
import { cn } from '@/shared/utils/general' // your utility for class merging
import { useAttrs } from 'vue'

const props = defineProps<{
  type: FieldType
  monochrome?: boolean
}>()

const attrs = useAttrs()

const displayText = {
  [FieldType.STRING]: 'String',
  [FieldType.INTEGER]: 'Integer',
  [FieldType.NUMBER]: 'Number',
  [FieldType.BOOLEAN]: 'Boolean',
  [FieldType.ARRAY]: 'Array',
  [FieldType.OBJECT]: 'Object',
}

const colorClass = {
  [FieldType.STRING]: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  [FieldType.INTEGER]: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  [FieldType.NUMBER]: 'bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200',
  [FieldType.BOOLEAN]: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  [FieldType.ARRAY]: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  [FieldType.OBJECT]: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
}

const baseClass = 'text-xs tracking-widest uppercase'

const finalClass = cn(
  baseClass,
  props.monochrome ? 'bg-muted text-foreground' : colorClass[props.type],
  attrs.class as string | undefined
)
</script>

<template>
  <Badge :class="finalClass" v-bind="{ ...attrs, class: undefined }">
    {{ displayText[type] }}
  </Badge>
</template>

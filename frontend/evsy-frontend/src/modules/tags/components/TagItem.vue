<script setup lang="ts">
import { ref } from 'vue'
import { Button } from '@/shared/components/ui/button'
import { Badge } from '@/shared/components/ui/badge'
import { Dialog, DialogTrigger, DialogContent } from '@/shared/components/ui/dialog'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  tag: { id: string; description?: string }
}>()

const isEditing = ref(false)
const isDeleting = ref(false)
</script>

<template>
  <div
    class="flex items-start justify-between gap-4 rounded-lg border p-4 transition hover:shadow-sm"
  >
    <div>
      <Badge variant="secondary" class="cursor-pointer" @click="">
        <span class="font-mono">#{{ tag.id }}</span>
      </Badge>
      <p v-if="tag.description" class="text-muted-foreground mt-1 text-sm">
        {{ tag.description }}
      </p>
    </div>

    <div class="flex gap-2">
      <Button size="icon" variant="ghost" @click="">
        <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
      </Button>
      <Button size="icon" variant="ghost" @click="">
        <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
      </Button>
    </div>
  </div>
</template>

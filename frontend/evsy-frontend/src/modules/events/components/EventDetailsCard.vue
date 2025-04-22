<script setup lang="ts">
import { ref } from 'vue'
import type { Event } from '@/modules/events/types'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/shared/components/ui/card'
import { Badge } from '@/shared/components/ui/badge'
import { Icon } from '@iconify/vue'
import { Button } from '@/shared/components/ui/button'
import EventEditModal from '@/modules/events/components/EventEditModal.vue'
import DeleteModal from '@/shared/components/data/DeleteModal.vue'
import { useAsyncTask } from '@/shared/composables/useAsyncTask'
import { eventApi } from '@/modules/events/api'
import { useApiErrorToast, useSuccessToast, useInfoToast } from '@/shared/utils/toast'
import { useRouter } from 'vue-router'
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/shared/components/ui/tooltip'
import { useClipboard } from '@vueuse/core'
import { computed } from 'vue'


const exampleValue = {
    user_id: 123,
    event_date: '2021-01-01',
    event_time: '2021-01-01T00:00:00Z',
    device: 'mobile',
    metadata: {
        source: 'landing',
        campaign: 'spring_sale',
    }
}
function getJsonPreview(obj: object, maxKeys = 2): string {
    const entries = Object.entries(obj)
    const limited = entries.slice(0, maxKeys)

    const formatted = limited
        .map(([key, value]) => {
            const val =
                typeof value === 'string'
                    ? `"${value}"`
                    : typeof value === 'object'
                        ? '{...}'
                        : value
            return `${key}: ${val}`
        })
        .join(', ')

    const suffix = entries.length > maxKeys ? ', ...' : ''
    return `{ ${formatted}${suffix} }`
}
const exampleShortPreview = computed(() => getJsonPreview(exampleValue))
const examplePrettyJson = computed(() => JSON.stringify(exampleValue, null, 2))

const props = defineProps<{
    event: Event
}>()

const emit = defineEmits<{
    (e: 'updated', event: Event): void
}>()

const router = useRouter()
const showEditModal = ref(false)
const showDeleteModal = ref(false)

const { isLoading: isDeleting, run: runDeleteTask } = useAsyncTask()
const { showSuccessToast } = useSuccessToast()
const { showApiErrorToast } = useApiErrorToast()
const { showInfoToast } = useInfoToast()

const handleUpdate = (updatedEvent: Event) => {
    emit('updated', updatedEvent)
}

const handleDelete = () => {
    runDeleteTask(async () => {
        await eventApi.delete(props.event.id)
        showSuccessToast('Event deleted successfully!')
        showDeleteModal.value = false
        router.push('/events')
    })
}


const { copy: copyId, isSupported } = useClipboard({ source: props.event.id.toString() })
const { copy: copyName } = useClipboard({ source: props.event.name })
const { copy: copyJson } = useClipboard({ source: examplePrettyJson })

const handleCopyId = async () => {
    try {
        await copyId()
        showInfoToast('ID copied to clipboard')
    } catch (err) {
        showApiErrorToast('Failed to copy ID')
    }
}

const handleCopyName = async () => {
    try {
        await copyName()
        showInfoToast('Name copied to clipboard')
    } catch (err) {
        showApiErrorToast('Failed to copy name')
    }
}

const handleCopyJson = async () => {
    try {
        await copyJson()
        showInfoToast('Name copied to clipboard')
    } catch (err) {
        showApiErrorToast('Failed to copy name')
    }
}
</script>

<template>
    <Card>
        <CardHeader>
            <div class="flex items-center justify-between">
                <!-- Title & ID -->
                <div class="flex items-center space-x-2">
                    <TooltipProvider :delay-duration="800">
                        <Tooltip>
                            <TooltipTrigger>
                                <CardTitle class="cursor-pointer font-mono text-xl tracking-wide"
                                    @click="handleCopyName">
                                    {{ event.name }}
                                </CardTitle>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Click to copy</p>
                            </TooltipContent>
                        </Tooltip>
                    </TooltipProvider>

                    <TooltipProvider :delay-duration="800">
                        <Tooltip>
                            <TooltipTrigger>
                                <Badge variant="outline" class="text-xs tracking-wide cursor-pointer"
                                    @click="handleCopyId">
                                    ID: {{ event.id }}
                                </Badge>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>Click to copy</p>
                            </TooltipContent>
                        </Tooltip>
                    </TooltipProvider>
                </div>

                <!-- Edit & Delete -->
                <div class="flex space-x-2">
                    <Button size="icon" variant="ghost" @click="showEditModal = true">
                        <Icon icon="radix-icons:pencil-2" class="h-4 w-4" />
                    </Button>
                    <Button size="icon" variant="ghost" @click="showDeleteModal = true">
                        <Icon icon="radix-icons:trash" class="text-destructive h-4 w-4" />
                    </Button>
                </div>
            </div>

            <CardDescription v-if="event.description">
                {{ event.description }}
            </CardDescription>

            <!-- Details section -->
            <div class="text-muted-foreground space-y-3 text-sm mt-4">
                <!-- Tags -->
                <div v-if="event.tags.length > 0" class="flex flex-wrap items-center gap-2">
                    <div class="flex items-center gap-1">
                        <Icon icon="radix-icons:component-1" class="h-4 w-4" />
                        <span>Tags:</span>
                    </div>
                    <Badge v-for="tag in event.tags" :key="tag.id" variant="secondary"
                        class="cursor-pointer font-mono tracking-wide" @click="router.push(`/tags/${tag.id}`)">
                        {{ tag.id }}
                    </Badge>
                </div>

                <!-- Example -->
                <TooltipProvider :delay-duration="200">
                    <Tooltip>
                        <TooltipTrigger>
                            <div class="flex items-center gap-2">
                                <Icon icon="radix-icons:file-text" class="h-4 w-4" />
                                <span>Example: <span class="font-mono">{{ exampleShortPreview }}</span></span>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" @click.stop
                            class=" max-h-64 overflow-y-auto text-xs text-left">
                            <button v-if="isSupported" @click="handleCopyJson"
                                class="absolute right-2 top-2 text-muted-foreground text-[10px] hover:underline">
                                <Icon icon="radix-icons:copy" class="inline h-3 w-3 mr-1" />
                            </button>
                            <div class="whitespace-pre-wrap font-mono leading-snug select-text">
                                {{ examplePrettyJson }}
                            </div>
                        </TooltipContent>
                    </Tooltip>
                </TooltipProvider>
            </div>
        </CardHeader>

        <CardContent>
            <div class="mt-4">
                <h3 class="mb-2 text-sm font-semibold text-muted-foreground">Associated Fields</h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-sm text-left border border-muted rounded-md">
                        <thead class="bg-muted/50">
                            <tr>
                                <th class="px-3 py-2">Name</th>
                                <th class="px-3 py-2">Type</th>
                                <th class="px-3 py-2">Description</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="field in event.fields" :key="field.id"
                                class="border-t border-muted hover:bg-muted/30">
                                <RouterLink :to="`/fields/${field.id}`" class="contents">
                                    <td class="px-3 py-2 font-mono">{{ field.name }}</td>
                                    <td class="px-3 py-2 capitalize">{{ field.field_type }}</td>
                                    <td class="px-3 py-2 text-muted-foreground">
                                        {{ field.description || '—' }}
                                    </td>
                                </RouterLink>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </CardContent>

        <!-- Modals -->
        <EventEditModal v-if="showEditModal" :event="event" @close="showEditModal = false" @updated="handleUpdate" />
        <DeleteModal :open="showDeleteModal" :onClose="() => (showDeleteModal = false)" :onConfirm="handleDelete"
            :isDeleting="isDeleting"
            description="Once deleted, this event will be unlinked from any tags or fields it's associated with." />
    </Card>
</template>

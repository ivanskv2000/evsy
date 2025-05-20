import type { Event } from '@/modules/events/types'
import type { JsonValue } from '@/modules/fields/types'
import { FieldType } from '@/modules/fields/types'
import { computed } from 'vue'

const fallbackExamples: Record<FieldType, JsonValue> = {
  [FieldType.STRING]: '',
  [FieldType.INTEGER]: 0,
  [FieldType.NUMBER]: 0.0,
  [FieldType.BOOLEAN]: true,
  [FieldType.ARRAY]: [],
  [FieldType.OBJECT]: {},
}

export function useEventExample(event: Event) {
  return computed(() => {
    const example: Record<string, JsonValue> = {}

    for (const field of event.fields) {
      example[field.name] = field.example ?? fallbackExamples[field.field_type]
    }

    return example
  })
}

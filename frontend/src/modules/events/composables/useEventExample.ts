import type { Field, JsonValue } from '@/modules/fields/types'
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

export function useEventExample(fields: Field[]) {
  return computed(() => {
    const example: Record<string, JsonValue> = {}
    for (const field of fields) {
      example[field.name] = field.example ?? fallbackExamples[field.field_type]
    }
    return example
  })
}

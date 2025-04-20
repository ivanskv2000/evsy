import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Field } from '../types'
import { fieldApi } from '../api'

export const useFieldsStore = defineStore('fields', () => {
  const fields = ref<Field[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const getFieldById = computed(() => (id: number) => 
    fields.value.find(field => field.id === id)
  )

  async function fetchFields() {
    loading.value = true
    error.value = null
    try {
      fields.value = await fieldApi.getAll()
    } catch (err: any) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function createField(data: Omit<Field, 'id'>) {
    loading.value = true
    error.value = null
    try {
      const newField = await fieldApi.create(data)
      fields.value.push(newField)
      return newField
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateField(id: number, data: Partial<Field>) {
    loading.value = true
    error.value = null
    try {
      const updatedField = await fieldApi.update(id, data)
      const index = fields.value.findIndex(field => field.id === id)
      if (index !== -1) {
        fields.value[index] = updatedField
      }
      return updatedField
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteField(id: number) {
    loading.value = true
    error.value = null
    try {
      await fieldApi.delete(id)
      fields.value = fields.value.filter(field => field.id !== id)
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    fields,
    loading,
    error,
    getFieldById,
    fetchFields,
    createField,
    updateField,
    deleteField,
  }
}) 
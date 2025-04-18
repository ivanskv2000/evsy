import { api } from "@/lib/api"
import type { Field } from "@/types"

export const fieldApi = {
    getAll(): Promise<Field[]> {
      return api.get<Field[]>("/fields")
    },
    
    getById(id: number): Promise<Field> {
      return api.get<Field>(`/fields/${id}`)
    },
    
    create(data: Omit<Field, "id">): Promise<Field> {
      return api.post<Field>("/fields", data)
    },
  
    update(id: number, data: Partial<Omit<Field, "id">>): Promise<Field> {
      return api.put<Field>(`/fields/${id}`, data)
    },
  
    delete(id: number): Promise<Field> {
      return api.delete<Field>(`/fields/${id}`)
    },
  }
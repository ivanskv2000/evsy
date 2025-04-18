import { toast } from "vue-sonner";


export function useSuccessToast(defaultTitle = "Success", defaultDescription = "Saved successfully") {
  function showSuccessToast(title?: string, description?: string) {
      toast.success(title || defaultTitle, {
        description: description || defaultDescription,
        duration: 3000,
      });
  }

  return { showSuccessToast };
}
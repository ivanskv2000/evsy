import { isAxiosError } from 'axios'

// Type definition that mirrors the backend's ErrorResponse Pydantic model
interface ApiErrorResponse {
  code: string
  message: string
  details?: {
    loc: (string | number)[]
    msg: string
    type: string
  }[]
}

/**
 * Type guard to check if the given data object conforms to the ApiErrorResponse structure.
 */
function isApiErrorResponse(data: unknown): data is ApiErrorResponse {
  return (
    typeof data === 'object' &&
    data !== null &&
    'code' in data &&
    'message' in data &&
    typeof (data as ApiErrorResponse).code === 'string' &&
    typeof (data as ApiErrorResponse).message === 'string'
  )
}

/**
 * Extracts a user-friendly message from an unknown error.
 * Designed to work with the standardized API error format.
 */
export function parseApiError(
  error: unknown,
  fallbackMessage = 'An unexpected error occurred'
): string {
  if (isAxiosError(error)) {
    // Handle network errors where there's no response from the server
    if (!error.response) {
      return 'Network Error: Could not connect to the server.'
    }

    const data = error.response.data

    // Check if the error response matches our standardized format
    if (isApiErrorResponse(data)) {
      // For validation errors, provide a more specific message from the details
      if (data.code === 'validation_error' && data.details?.length) {
        const firstDetail = data.details[0]
        // Example: "name: Field required"
        const fieldName = firstDetail.loc.slice(-1)[0]
        return `${fieldName}: ${firstDetail.msg}`
      }
      // For all other standard API errors, use the main message
      return data.message
    }
  }

  // Handle generic JavaScript errors (e.g., new Error('...'))
  if (error instanceof Error) {
    return error.message
  }

  // If the error is in an unknown format, return the fallback message
  return fallbackMessage
}

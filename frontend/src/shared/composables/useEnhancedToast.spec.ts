import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useEnhancedToast } from './useEnhancedToast'

const mockToast = vi.hoisted(() => {
  return {
  error: vi.fn(),
  success: vi.fn(),
  info: vi.fn(),
}
})

vi.mock('vue-sonner', () => ({
  toast: mockToast,
}))

const mockParseApiError = vi.hoisted(() => vi.fn())

vi.mock('@/shared/utils/parseApiError', () => ({
  parseApiError: mockParseApiError,
}))

describe('useEnhancedToast', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  const { showError, showSuccess, showInfo, showCreated, showCopied } = useEnhancedToast()

  describe('showError', () => {
    it('should parse the error and show an error toast with the parsed message', () => {
      // Arrange
      const error = new Error('A wild bug appears!')
      const parsedMessage = 'This is a parsed error message.'
      mockParseApiError.mockReturnValue(parsedMessage)

      // Act
      showError(error, 'Custom Error Title')

      // Assert
      // 1. Check if the error was parsed
      expect(mockParseApiError).toHaveBeenCalledWith(error)
      // 2. Check if the toast was called with the correct arguments
      expect(mockToast.error).toHaveBeenCalledWith('Custom Error Title', {
        description: parsedMessage,
        duration: 5000,
      })
    })
  })

  describe('showSuccess', () => {
    it('should show a success toast with the provided title and description', () => {
      // Act
      showSuccess('Operation Complete', 'Your data has been saved.')

      // Assert
      expect(mockToast.success).toHaveBeenCalledWith('Operation Complete', {
        description: 'Your data has been saved.',
        duration: 3000,
      })
    })
  })

  describe('showInfo', () => {
    it('should show an info toast with the provided title and description', () => {
      // Act
      showInfo('Just so you know', 'This is an informational message.')

      // Assert
      expect(mockToast.info).toHaveBeenCalledWith('Just so you know', {
        description: 'This is an informational message.',
        duration: 3000,
      })
    })
  })

  describe('Common Toast Utilities', () => {
    it('showCreated should call showSuccess with a formatted message', () => {
      // Act
      showCreated('New User')

      // Assert
      expect(mockToast.success).toHaveBeenCalledWith('New User created successfully!', {
        description: undefined,
        duration: 3000,
      })
    })

    it('showCopied should call showInfo with a formatted message', () => {
      // Act
      showCopied('API Key')

      // Assert
      expect(mockToast.info).toHaveBeenCalledWith('API Key copied to clipboard', {
        description: undefined,
        duration: 3000,
      })
    })
  })
})

import { describe, it, expect, vi, beforeEach, type Mock } from 'vitest'
import { mount } from '@vue/test-utils'
import SyncStatusButton from './SyncStatusButton.vue'
import { useIsFetching, useQueryClient, onlineManager } from '@tanstack/vue-query'
import { useEnhancedToast } from '@/shared/composables/useEnhancedToast'

// Mock TanStack Query
vi.mock('@tanstack/vue-query', () => ({
  useIsFetching: vi.fn(),
  useQueryClient: vi.fn(),
  onlineManager: {
    isOnline: vi.fn(),
  },
}))

// Mock Enhanced Toast
vi.mock('@/shared/composables/useEnhancedToast', () => ({
  useEnhancedToast: vi.fn(),
}))

// Mock Iconify
vi.mock('@iconify/vue', () => ({
  Icon: { template: '<span>icon</span>' },
}))

describe('SyncStatusButton', () => {
  let mockQueryClient: { invalidateQueries: Mock }
  let mockShowSuccess: Mock
  let mockShowError: Mock

  beforeEach(() => {
    vi.clearAllMocks()

    mockQueryClient = {
      invalidateQueries: vi.fn().mockResolvedValue(undefined),
    }
    ;(useQueryClient as Mock).mockReturnValue(mockQueryClient)
    ;(useIsFetching as Mock).mockReturnValue({ value: 0 })
    ;(onlineManager.isOnline as Mock).mockReturnValue(true)

    mockShowSuccess = vi.fn()
    mockShowError = vi.fn()
    ;(useEnhancedToast as Mock).mockReturnValue({
      showSuccess: mockShowSuccess,
      showError: mockShowError,
    })

    // Silence console during tests if needed
    vi.spyOn(console, 'error').mockImplementation(() => {})
  })

  it('should call invalidateQueries and show success toast on click when online', async () => {
    vi.useFakeTimers()
    const wrapper = mount(SyncStatusButton, {
      global: {
        stubs: {
          TooltipProvider: { template: '<div><slot /></div>' },
          Tooltip: { template: '<div><slot /></div>' },
          TooltipTrigger: { template: '<div><slot /></div>' },
          TooltipContent: { template: '<div><slot /></div>' },
          Button: {
            template: '<button @click="$emit(\'click\')"><slot /></button>',
            props: ['disabled'],
          },
        },
      },
    })

    const button = wrapper.find('button')
    await button.trigger('click')

    // After click, it should have started invalidation
    expect(mockQueryClient.invalidateQueries).toHaveBeenCalled()

    // Wait for the minimum duration (600ms)
    await vi.advanceTimersByTimeAsync(600)

    expect(mockShowSuccess).toHaveBeenCalledWith(
      'Data is updated successfully!'
    )
    vi.useRealTimers()
  })

  it('should show "Sync Paused" error when offline after click', async () => {
    vi.useFakeTimers()
    ;(onlineManager.isOnline as Mock).mockReturnValue(false)

    const wrapper = mount(SyncStatusButton, {
      global: {
        stubs: {
          TooltipProvider: { template: '<div><slot /></div>' },
          Tooltip: { template: '<div><slot /></div>' },
          TooltipTrigger: { template: '<div><slot /></div>' },
          TooltipContent: { template: '<div><slot /></div>' },
          Button: {
            template: '<button @click="$emit(\'click\')"><slot /></button>',
            props: ['disabled'],
          },
        },
      },
    })

    const button = wrapper.find('button')
    await button.trigger('click')

    await vi.advanceTimersByTimeAsync(600)

    expect(mockShowError).toHaveBeenCalled()
    const errorPassed = mockShowError.mock.calls[0][0]
    expect(errorPassed.message).toContain('currently offline')
    vi.useRealTimers()
  })

  it('should NOT call showError on query failure (relying on global handler)', async () => {
    vi.useFakeTimers()
    const error = new Error('Network error')
    mockQueryClient.invalidateQueries.mockRejectedValue(error)

    const wrapper = mount(SyncStatusButton, {
      global: {
        stubs: {
          TooltipProvider: { template: '<div><slot /></div>' },
          Tooltip: { template: '<div><slot /></div>' },
          TooltipTrigger: { template: '<div><slot /></div>' },
          TooltipContent: { template: '<div><slot /></div>' },
          Button: {
            template: '<button @click="$emit(\'click\')"><slot /></button>',
            props: ['disabled'],
          },
        },
      },
    })

    const button = wrapper.find('button')
    await button.trigger('click')

    await vi.advanceTimersByTimeAsync(600)

    expect(mockShowError).not.toHaveBeenCalled()
    vi.useRealTimers()
  })
})

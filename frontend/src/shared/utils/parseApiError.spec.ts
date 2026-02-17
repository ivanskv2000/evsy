import { AxiosError, AxiosHeaders } from 'axios'
import { describe, it, expect } from 'vitest'
import { parseApiError } from './parseApiError'

describe('parseApiError', () => {
  it('should return the message from a standard API error response', () => {
    const mockError = new AxiosError('Request failed', 'ERR_BAD_REQUEST', undefined, undefined, {
      data: { code: 'not_found', message: 'The requested item was not found.' },
      status: 404,
      statusText: 'Not Found',
      headers: {},
      config: { headers: new AxiosHeaders() },
    })

    expect(parseApiError(mockError)).toBe('The requested item was not found.')
  })

  it('should parse and format a validation error from the details', () => {
    const mockError = new AxiosError('Request failed', 'ERR_BAD_REQUEST', undefined, undefined, {
      data: {
        code: 'validation_error',
        message: 'Input validation failed.',
        details: [{ loc: ['body', 'email'], msg: 'must be a valid email address', type: 'string' }],
      },
      status: 422,
      statusText: 'Unprocessable Entity',
      headers: {},
      config: { headers: new AxiosHeaders() },
    })

    expect(parseApiError(mockError)).toBe('email: must be a valid email address')
  })

  it('should return a specific message for a network error (no response)', () => {
    const mockError = new AxiosError('Network Error', 'ERR_NETWORK') // simulates a network failure

    expect(parseApiError(mockError)).toBe('Network Error: Could not connect to the server.')
  })

  it('should return the message from a generic JavaScript Error', () => {
    const genericError = new Error('Something went wrong in the browser')
    expect(parseApiError(genericError)).toBe('Something went wrong in the browser')
  })

  it('should return the default fallback message for an unknown error type', () => {
    const unknownError = { some: 'random object' }
    expect(parseApiError(unknownError)).toBe('An unexpected error occurred')
  })

  it('should return the message from a non-standard Axios error', () => {
    const mockError = new AxiosError('Something went wrong on the backend', 'ERR_BAD_REQUEST', undefined, undefined, {
      data: { error: 'This is not the format we expect' }, // non-compliant data
      status: 500,
      statusText: 'Internal Server Error',
      headers: {},
      config: { headers: new AxiosHeaders() },
    })

    expect(parseApiError(mockError)).toBe('Something went wrong on the backend')
  })

  it('should return a custom fallback message when provided', () => {
    const unknownError = 'just a string error'
    const customMessage = 'Oops! Something failed. Please try again.'
    expect(parseApiError(unknownError, customMessage)).toBe(customMessage)
  })
})

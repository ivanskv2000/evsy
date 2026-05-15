import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useDataTableUrlSync, type SyncConfig } from './useDataTableUrlSync'
import { useRoute, useRouter } from 'vue-router'

// Mock vue-router to control route state and spy on navigation
vi.mock('vue-router', () => ({
  useRoute: vi.fn(),
  useRouter: vi.fn(),
}))

describe('useDataTableUrlSync', () => {
  const mockRouter = {
    replace: vi.fn(),
  }

  const defaultConfig: SyncConfig = {
    columnFilters: {
      name: { param: 'search' },
      tags: { param: 'tag', type: 'array' },
    },
    sorting: {
      sortParam: 'sort',
      orderParam: 'order',
    },
  }

  beforeEach(() => {
    vi.clearAllMocks()
    // Default setup for each test
    /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
    ;(useRouter as any).mockReturnValue(mockRouter)
  })

  describe('URL-to-Table State', () => {
    it('should correctly parse sorting state from mocked route query', () => {
      // GIVEN the URL has sort and order params
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({
        query: { sort: 'name', order: 'desc' },
      })

      // WHEN we initialize the sync
      const { state } = useDataTableUrlSync(defaultConfig)

      // THEN it should return TanStack compatible sorting state
      expect(state.sorting.value).toEqual([{ id: 'name', desc: true }])
    })

    it('should correctly parse string and array column filters from URL', () => {
      // GIVEN a search string and a comma-separated list in the URL
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({
        query: { search: 'test-query', tag: 'frontend,testing' },
      })

      const { state } = useDataTableUrlSync(defaultConfig)

      // THEN it should split the array and keep the string intact
      expect(state.columnFilters.value).toEqual([
        { id: 'name', value: 'test-query' },
        { id: 'tags', value: ['frontend', 'testing'] },
      ])
    })
  })

  describe('Table-to-URL Updaters', () => {
    it('should invoke router.replace with mapped parameters on sorting change', () => {
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({ query: {} })

      const { updaters } = useDataTableUrlSync(defaultConfig)

      // WHEN the table triggers a sorting change
      updaters.onSortingChange([{ id: 'id', desc: false }])

      // THEN it should push the correct params to the URL
      expect(mockRouter.replace).toHaveBeenCalledWith({
        query: { sort: 'id', order: 'asc' },
      })
    })

    it('should join array filters into a comma-separated string when updating URL', () => {
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({ query: {} })

      const { updaters } = useDataTableUrlSync(defaultConfig)

      // WHEN the table triggers a filter change
      updaters.onColumnFiltersChange([
        { id: 'name', value: 'vuejs' },
        { id: 'tags', value: ['refactor', 'clean-code'] },
      ])

      // THEN it should map them back to the query params
      expect(mockRouter.replace).toHaveBeenCalledWith({
        query: { search: 'vuejs', tag: 'refactor,clean-code' },
      })
    })

    it('should support functional updaters (standard TanStack pattern)', () => {
      // GIVEN an existing state in the URL
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({
        query: { sort: 'name', order: 'asc' },
      })

      const { updaters } = useDataTableUrlSync(defaultConfig)

      // WHEN we use a functional updater to toggle the direction
      updaters.onSortingChange((old) => [{ id: old[0].id, desc: !old[0].desc }])

      // THEN it should calculate the new state based on old and update URL
      expect(mockRouter.replace).toHaveBeenCalledWith({
        query: { sort: 'name', order: 'desc' },
      })
    })
  })

  describe('Empty States', () => {
    it('should return safe empty arrays when URL query is empty', () => {
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({ query: {} })

      const { state } = useDataTableUrlSync(defaultConfig)
      expect(state.sorting.value).toEqual([])
      expect(state.columnFilters.value).toEqual([])
    })

    it('should remove parameters from URL when state is cleared (empty array provided)', () => {
      // GIVEN there are existing params
      /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
      ;(useRoute as any).mockReturnValue({
        query: { sort: 'name', search: 'test' },
      })

      const { updaters } = useDataTableUrlSync(defaultConfig)

      // WHEN we clear the sorting
      updaters.onSortingChange([])

      // THEN the sort params should be deleted from the final query
      expect(mockRouter.replace).toHaveBeenCalledWith({
        query: { search: 'test' },
      })
    })
  })
})

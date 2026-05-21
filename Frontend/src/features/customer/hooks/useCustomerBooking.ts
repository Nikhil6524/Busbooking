import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  cancelCustomerBooking,
  createCustomerBooking,
  fetchCustomerCurrentBooking,
  fetchCustomerInitialData,
  fetchCustomerSeatMap,
  fetchCustomerFavorites,
  addCustomerFavorite,
  removeCustomerFavorite,
  searchCustomerJourneys,
} from '../services/customerBookingService'
import { buildSeatLabels, formatDate, formatTime, isActiveSchedule } from '../utils/customerBookingUtils'
import {
  initialSearchForm,
  type BookingRecord,
  type CurrentBookingRecord,
  type CurrentBookingList,
  type ScheduleRecord,
  type SeatMapResponse,
  type SearchFormState,
  type SectionStatus,
} from '../context/CustomerBookingTypes'

export function useCustomerBooking(businessBase: string) {
  const seatSectionRef = useRef<HTMLElement | null>(null)
  const [buses, setBuses] = useState<ScheduleRecord[]>([])
  const [searchForm, setSearchForm] = useState<SearchFormState>(initialSearchForm)
  const [results, setResults] = useState<ScheduleRecord[]>([])
  const [bookings, setBookings] = useState<BookingRecord[]>([])
  const [favorites, setFavorites] = useState<number[]>([])
  const [currentBookings, setCurrentBookings] = useState<CurrentBookingList>([])
  const [showCurrentBooking, setShowCurrentBooking] = useState(false)
  const [showHistory, setShowHistory] = useState(false)
  const [selectedSchedule, setSelectedSchedule] = useState<ScheduleRecord | null>(null)
  const [seatMap, setSeatMap] = useState<SeatMapResponse | null>(null)
  const [selectedSeat, setSelectedSeat] = useState('')
  const [loading, setLoading] = useState(false)
  const [cancellingBookingId, setCancellingBookingId] = useState('')
  const [status, setStatus] = useState<SectionStatus>({ type: 'idle', message: '' })
  const [bookingStatus, setBookingStatus] = useState<SectionStatus>({ type: 'idle', message: '' })

  const clearSeatSelection = useCallback(() => {
    setSelectedSchedule(null)
    setSeatMap(null)
    setSelectedSeat('')
  }, [])

  const loadSearchResults = useCallback(async () => {
    if (!searchForm.source.trim() || !searchForm.destination.trim() || !searchForm.journeyDate.trim()) {
      setStatus({ type: 'error', message: 'Invalid input.' })
      return
    }

    setLoading(true)
    setStatus({ type: 'loading', message: 'Searching journeys...' })
    clearSeatSelection()

    try {
      let journeys = await searchCustomerJourneys(businessBase, searchForm)
      // If backend returned no results (exact match failed), try a fuzzy client-side fallback
      if (journeys && journeys.length === 0) {
        try {
          const initial = await fetchCustomerInitialData(businessBase)
          journeys = initial.buses.filter((record) => record.schedule.journey_date === searchForm.journeyDate)
        } catch {
          journeys = []
        }
      }
      if (!journeys) {
        setResults([])
        setStatus({ type: 'error', message: 'Invalid input.' })
        return
      }

      const active = journeys.filter((record) => isActiveSchedule(record.schedule.status))
      // apply fuzzy destination matching to narrow results
      const { fuzzyMatch } = await import('../utils/customerBookingUtils')
      const filtered = active.filter((record) => fuzzyMatch(record.route.destination, searchForm.destination))
      const prioritized = [...filtered].sort((a, b) => {
        const ai = favorites.indexOf(a.bus.id)
        const bi = favorites.indexOf(b.bus.id)
        if (ai === -1 && bi === -1) return 0
        if (ai === -1) return 1
        if (bi === -1) return -1
        return ai - bi
      })
      setResults(prioritized)
      setStatus({ type: 'success', message: 'Journeys loaded successfully.' })
    } catch {
      setResults([])
      setStatus({ type: 'error', message: 'Invalid input.' })
    } finally {
      setLoading(false)
    }
  }, [businessBase, clearSeatSelection, searchForm, favorites])

  const loadBookings = useCallback(async () => {
    try {
      const initialData = await fetchCustomerInitialData(businessBase)
      setBookings(initialData.bookings)
    } catch {
      setBookings([])
    }
  }, [businessBase])

  const loadFavorites = useCallback(async () => {
    try {
      const favs = await fetchCustomerFavorites(businessBase)
      const ids = favs.map((f) => f.bus_id)
      setFavorites(ids)
    } catch {
      setFavorites([])
    }
  }, [businessBase])

  const loadCurrentBooking = useCallback(async () => {
    try {
      const bookings = await fetchCustomerCurrentBooking(businessBase)
      setCurrentBookings(bookings)
    } catch {
      setCurrentBookings([])
    }
  }, [businessBase])

  const toggleFavorite = useCallback(
    async (busId: number) => {
      const isFav = favorites.includes(busId)
      // optimistic update
      setFavorites((prev) => (isFav ? prev.filter((id) => id !== busId) : [busId, ...prev]))
      try {
        if (isFav) {
          await removeCustomerFavorite(businessBase, busId)
        } else {
          await addCustomerFavorite(businessBase, busId)
        }
      } catch {
        // revert on error
        setFavorites((prev) => (isFav ? [busId, ...prev] : prev.filter((id) => id !== busId)))
      }
    },
    [businessBase, favorites]
  )

  const loadSeatMap = useCallback(
    async (record: ScheduleRecord) => {
      if (!isActiveSchedule(record.schedule.status)) {
        setStatus({ type: 'error', message: 'This journey is not available.' })
        return
      }

      setSelectedSchedule(record)
      setSeatMap(null)
      setSelectedSeat('')
      setBookingStatus({ type: 'idle', message: '' })

      const seatMapResponse = await fetchCustomerSeatMap(businessBase, record.schedule.id)
      if (!seatMapResponse) {
        setStatus({ type: 'error', message: 'Invalid input.' })
        return
      }

      setSeatMap(seatMapResponse)
      seatSectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    },
    [businessBase]
  )

  const bookSeat = useCallback(async () => {
    if (!selectedSchedule || !selectedSeat.trim()) {
      setBookingStatus({ type: 'error', message: 'Invalid input.' })
      return
    }

    setBookingStatus({ type: 'loading', message: 'Booking seat...' })
    try {
      const success = await createCustomerBooking(businessBase, selectedSchedule.schedule.id, selectedSeat)

      if (!success) {
        setBookingStatus({ type: 'error', message: 'Invalid input.' })
        return
      }

      setBookingStatus({ type: 'success', message: 'Seat booked successfully.' })
      setShowCurrentBooking(true)
      await loadSeatMap(selectedSchedule)
      await loadSearchResults()
      await loadCurrentBooking()
    } catch {
      setBookingStatus({ type: 'error', message: 'Invalid input.' })
    }
  }, [businessBase, loadCurrentBooking, loadSearchResults, loadSeatMap, selectedSchedule, selectedSeat])

  const cancelBooking = useCallback(
    async (bookingId: string) => {
      setCancellingBookingId(bookingId)
      try {
        const success = await cancelCustomerBooking(businessBase, bookingId)
        if (!success) {
          setStatus({ type: 'error', message: 'Unable to cancel booking.' })
          return
        }

        setStatus({ type: 'success', message: 'Booking cancelled successfully.' })
        await loadBookings()
        await loadSearchResults()
        await loadCurrentBooking()

        if (selectedSchedule) {
          await loadSeatMap(selectedSchedule)
        }
      } catch {
        setStatus({ type: 'error', message: 'Unable to cancel booking.' })
      } finally {
        setCancellingBookingId('')
      }
    },
    [businessBase, loadBookings, loadSearchResults, loadSeatMap, selectedSchedule]
  )

  const selectedBusLabel = useMemo(() => {
    if (!selectedSchedule) {
      return '-'
    }

    return `${selectedSchedule.bus.bus_name} (${selectedSchedule.bus.bus_number})`
  }, [selectedSchedule])

  const toggleHistory = useCallback(async () => {
    setShowHistory((current) => !current)
    if (!showHistory && !bookings.length) {
      await loadBookings()
    }
  }, [bookings.length, loadBookings, showHistory])

  const toggleCurrentBooking = useCallback(async () => {
    setShowCurrentBooking((current) => !current)
    if (!showCurrentBooking && !currentBookings.length) {
      await loadCurrentBooking()
    }
  }, [currentBookings.length, loadCurrentBooking, showCurrentBooking])

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const initialData = await fetchCustomerInitialData(businessBase)
        const favs = await fetchCustomerFavorites(businessBase)
        const favIds = favs.map((f) => f.bus_id)
        setFavorites(favIds)
        const active = initialData.buses.filter((record) => isActiveSchedule(record.schedule.status))
        // place favorite buses at top in the same order as favorites
        const prioritized = [...active].sort((a, b) => {
          const ai = favIds.indexOf(a.bus.id)
          const bi = favIds.indexOf(b.bus.id)
          if (ai === -1 && bi === -1) return 0
          if (ai === -1) return 1
          if (bi === -1) return -1
          return ai - bi
        })
        setBuses(prioritized)
        setBookings(initialData.bookings)
      } catch {
        setBuses([])
        setBookings([])
      }
    }

    void loadInitialData()
  }, [businessBase])

  return {
    bookingStatus,
    bookings,
    buses,
    favorites,
    cancelBooking,
    cancellingBookingId,
    currentBookings,
    formatDate,
    formatTime,
    isActiveSchedule,
    loadSearchResults,
    loadSeatMap,
    toggleFavorite,
    loading,
    results,
    searchForm,
    seatMap,
    seatSectionRef,
    selectedBusLabel,
    selectedSchedule,
    selectedSeat,
    setSearchForm,
    setSelectedSeat,
    setShowHistory,
    showCurrentBooking,
    showHistory,
    status,
    toggleCurrentBooking,
    toggleHistory,
    bookSeat,
    buildSeatLabels,
    buildSeatRows: (seats: string[]) => {
      const rows: string[][] = []
      const groupSize = 4
      for (let index = 0; index < seats.length; index += groupSize) {
        rows.push(seats.slice(index, index + groupSize))
      }
      return rows
    },
  }
}

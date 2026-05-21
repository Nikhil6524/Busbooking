import { useCallback, useEffect, useMemo, useState } from 'react'

import {
  addDashboardEntity,
  fetchDashboardRecords,
  toggleDashboardScheduleStatus,
  updateDashboardEntity,
} from '../services/adminDashboardService'
import { getBusIds, normalize } from '../utils/adminDashboardUtils'
import {
  initialJourneyForm,
  type JourneyFormState,
  type RouteRecord,
  type ScheduleRecord,
  type SectionStatus,
} from '../context/AdminDashboardTypes'

export function useAdminDashboard(businessBase: string) {
  const [journeys, setJourneys] = useState<ScheduleRecord[]>([])
  const [routes, setRoutes] = useState<RouteRecord[]>([])
  const [form, setForm] = useState<JourneyFormState>(initialJourneyForm)
  const [status, setStatus] = useState<SectionStatus>({ type: 'idle', message: '' })
  const [loading, setLoading] = useState(false)
  const [updatingScheduleId, setUpdatingScheduleId] = useState<number | null>(null)
  const [editingBusId, setEditingBusId] = useState<number | null>(null)

  const loadRecords = useCallback(async () => {
    setLoading(true)
    try {
      const records = await fetchDashboardRecords(businessBase)
      setRoutes(records.routes)
      setJourneys(records.journeys)
    } finally {
      setLoading(false)
    }
  }, [businessBase])

  useEffect(() => {
    const loadInitialRecords = async () => {
      setLoading(true)
      try {
        const records = await fetchDashboardRecords(businessBase)
        setRoutes(records.routes)
        setJourneys(records.journeys)
      } finally {
        setLoading(false)
      }
    }

    void loadInitialRecords()
  }, [businessBase])

  const busIds = useMemo(() => getBusIds(journeys), [journeys])

  const upsertBus = useCallback(
    async (busId: number) => {
      const busPayload = {
        id: busId,
        bus_name: form.busName.trim(),
        bus_number: form.busNumber.trim(),
        bus_type: form.busType.trim() || null,
        total_seats: Number(form.totalSeats),
        operator_name: form.operatorName.trim() || null,
        amenities: form.amenities.trim() || null,
      }

      // Try to update existing bus first. If update fails, create a new bus.
      const updatedBus = await updateDashboardEntity<unknown>(businessBase, 'bus', busId, busPayload)
      if (updatedBus) return true

      // Remove id when creating a new bus payload to avoid accidental conflicts.
      // The backend will assign an id for newly created entities.
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { id, ...createPayload } = busPayload as unknown as { id?: number }
      const createdBus = await addDashboardEntity<unknown>(businessBase, 'bus', createPayload)
      return Boolean(createdBus)
    },
    [businessBase, form.amenities, form.busName, form.busNumber, form.busType, form.operatorName, form.totalSeats]
  )

  const upsertRoute = useCallback(
    async (busId: number) => {
      const routePayload = {
        bus_id: busId,
        source: form.source.trim(),
        destination: form.destination.trim(),
        distance: form.distance.trim() ? Number(form.distance) : null,
        duration: form.duration.trim() || null,
      }

      const existingRoute = routes.find((route) =>
        route.bus_id === busId &&
        normalize(route.source) === normalize(form.source) &&
        normalize(route.destination) === normalize(form.destination)
      )

      if (existingRoute) {
        const updatedRoute = await updateDashboardEntity<unknown>(businessBase, 'route', existingRoute.id, routePayload)
        if (updatedRoute) {
          return existingRoute.id
        }
      }

      const createdRoute = await addDashboardEntity<{ id: number }>(businessBase, 'route', routePayload)
      return createdRoute ? createdRoute.id : null
    },
    [businessBase, form.destination, form.distance, form.duration, form.source, routes]
  )

  const upsertSchedule = useCallback(
    async (busId: number, routeId: number) => {
      const schedulePayload = {
        bus_id: busId,
        route_id: routeId,
        departure_time: form.departureTime,
        arrival_time: form.arrivalTime,
        journey_date: form.journeyDate,
        price: Number(form.price),
        available_seats: Number(form.availableSeats),
        status: form.status.trim() || null,
      }

      const existingSchedule = journeys.find((item) =>
        item.bus.id === busId &&
        item.route.id === routeId &&
        item.schedule.journey_date === form.journeyDate
      )

      if (existingSchedule) {
        const updatedSchedule = await updateDashboardEntity<unknown>(
          businessBase,
          'schedule',
          existingSchedule.schedule.id,
          schedulePayload
        )
        return Boolean(updatedSchedule)
      }

      const createdSchedule = await addDashboardEntity<unknown>(businessBase, 'schedule', schedulePayload)
      return Boolean(createdSchedule)
    },
    [businessBase, form.arrivalTime, form.availableSeats, form.departureTime, form.journeyDate, form.price, form.status, journeys]
  )

  const submitJourneyEntity = useCallback(async () => {
    if (
      !form.busId.trim() ||
      !form.busName.trim() ||
      !form.busNumber.trim() ||
      !form.totalSeats.trim() ||
      !form.source.trim() ||
      !form.destination.trim() ||
      !form.departureTime.trim() ||
      !form.arrivalTime.trim() ||
      !form.journeyDate.trim() ||
      !form.price.trim() ||
      !form.availableSeats.trim()
    ) {
      setStatus({ type: 'error', message: 'Invalid input.' })
      return
    }

    const busId = Number(form.busId)
    if (!Number.isFinite(busId) || busId <= 0) {
      setStatus({ type: 'error', message: 'Invalid input.' })
      return
    }

    setStatus({ type: 'loading', message: 'Saving journey entity...' })

    try {
      // If admin is editing an existing bus, prefer explicit update to avoid accidental creates.
      let busSaved = false
      const busPayload = {
        id: busId,
        bus_name: form.busName.trim(),
        bus_number: form.busNumber.trim(),
        bus_type: form.busType.trim() || null,
        total_seats: Number(form.totalSeats),
        operator_name: form.operatorName.trim() || null,
        amenities: form.amenities.trim() || null,
      }

      if (editingBusId) {
        const updated = await updateDashboardEntity<unknown>(businessBase, 'bus', editingBusId, busPayload)
        busSaved = Boolean(updated)
      } else {
        busSaved = await upsertBus(busId)
      }

      if (!busSaved) {
        setStatus({ type: 'error', message: 'Invalid input.' })
        return
      }

      const routeId = await upsertRoute(busId)
      if (!routeId) {
        setStatus({ type: 'error', message: 'Invalid input.' })
        return
      }

      const scheduleSaved = await upsertSchedule(busId, routeId)
      setStatus(
        scheduleSaved
          ? { type: 'success', message: 'Journey entity saved successfully.' }
          : { type: 'error', message: 'Invalid input.' }
      )

      if (scheduleSaved) {
        setForm(initialJourneyForm)
        setEditingBusId(null)
        await loadRecords()
      }
    } catch {
      setStatus({ type: 'error', message: 'Invalid input.' })
    }
  }, [form, loadRecords, upsertBus, upsertRoute, upsertSchedule])

  const toggleScheduleStatus = useCallback(
    async (schedule: ScheduleRecord['schedule']) => {
      const currentStatus = normalize(schedule.status ?? '')
      const nextStatus = currentStatus === 'active' ? 'inactive' : 'active'

      setUpdatingScheduleId(schedule.id)
      try {
        const ok = await toggleDashboardScheduleStatus(businessBase, schedule.id, nextStatus)

        setStatus(
          ok
            ? { type: 'success', message: `Schedule ${schedule.id} marked as ${nextStatus}.` }
            : { type: 'error', message: 'Unable to update schedule status.' }
        )

        if (ok) {
          await loadRecords()
        }
      } catch {
        setStatus({ type: 'error', message: 'Unable to update schedule status.' })
      } finally {
        setUpdatingScheduleId(null)
      }
    },
    [businessBase, loadRecords]
  )

  return {
    busIds,
    form,
    journeys,
    loading,
    routes,
    setForm,
    status,
    submitJourneyEntity,
    toggleScheduleStatus,
    updatingScheduleId,
    editingBusId,
    setEditingBusId,
  }
}
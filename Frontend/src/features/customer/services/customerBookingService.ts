import type {
  BookingRecord,
  CurrentBookingRecord,
  CurrentBookingList,
  RouteRecord,
  ScheduleRecord,
  SeatMapResponse,
  SearchFormState,
} from '../context/CustomerBookingTypes'

type RequestJsonResult = {
  ok: boolean
  data: unknown
  status: number
}

async function requestJson(url: string, method: string, body?: unknown): Promise<RequestJsonResult> {
  const token = window.localStorage.getItem('busbook-token')
  const response = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    credentials: 'include',
    body: body ? JSON.stringify(body) : undefined,
  })

  const contentType = response.headers.get('content-type') ?? ''
  let data: unknown

  try {
    data = contentType.includes('application/json') ? await response.json() : await response.text()
  } catch {
    data = await response.text()
  }

  return { ok: response.ok, data, status: response.status }
}

export async function fetchCustomerInitialData(businessBase: string) {
  const [busesResponse, bookingsResponse] = await Promise.all([
    requestJson(`${businessBase}/schedules/details/all`, 'GET'),
    requestJson(`${businessBase}/bookings/history`, 'GET'),
  ])

  return {
    buses: busesResponse.ok ? (busesResponse.data as ScheduleRecord[]) : [],
    bookings: bookingsResponse.ok ? (bookingsResponse.data as BookingRecord[]) : [],
  }
}

export async function fetchCustomerCurrentBooking(businessBase: string) {
  const response = await requestJson(`${businessBase}/bookings/current`, 'GET')
  if (!response.ok || response.data === null) {
    return []
  }

  return response.data as CurrentBookingList
}

export async function searchCustomerJourneys(businessBase: string, form: SearchFormState) {
  const query = new URLSearchParams({
    source: form.source.trim(),
    destination: form.destination.trim(),
    journey_date: form.journeyDate,
  })

  const response = await requestJson(`${businessBase}/schedules/search/combined?${query.toString()}`, 'GET')
  return response.ok ? (response.data as ScheduleRecord[]) : null
}

export async function fetchCustomerSeatMap(businessBase: string, scheduleId: number) {
  const response = await requestJson(`${businessBase}/schedules/${scheduleId}/seats`, 'GET')
  return response.ok ? (response.data as SeatMapResponse) : null
}

export async function fetchCustomerFavorites(businessBase: string) {
  const response = await requestJson(`${businessBase}/favorites`, 'GET')
  return response.ok ? (response.data as { bus_id: number; id: number }[]) : []
}

export async function addCustomerFavorite(businessBase: string, busId: number) {
  const response = await requestJson(`${businessBase}/favorites`, 'POST', { bus_id: busId })
  return response.ok
}

export async function removeCustomerFavorite(businessBase: string, busId: number) {
  const response = await requestJson(`${businessBase}/favorites/${busId}`, 'DELETE')
  return response.ok
}

export async function createCustomerBooking(businessBase: string, scheduleId: number, seatNumber: string) {
  const response = await requestJson(`${businessBase}/bookings`, 'POST', {
    schedule_id: scheduleId,
    seat_number: seatNumber,
  })

  return response.ok
}

export async function cancelCustomerBooking(businessBase: string, bookingId: string) {
  const response = await requestJson(`${businessBase}/bookings/${bookingId}`, 'DELETE')
  return response.ok
}

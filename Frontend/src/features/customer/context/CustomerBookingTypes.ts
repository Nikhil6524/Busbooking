export type BusRecord = {
  id: number
  bus_name: string
  bus_number: string
  bus_type: string | null
  total_seats: number
  operator_name: string | null
  amenities: string | null
}

export type RouteRecord = {
  id: number
  bus_id: number
  source: string
  destination: string
  distance: number | null
  duration: string | null
}

export type ScheduleRecord = {
  bus: BusRecord
  route: RouteRecord
  schedule: {
    id: number
    bus_id: number
    route_id: number
    departure_time: string
    arrival_time: string
    journey_date: string
    price: number
    available_seats: number
    status: string | null
  }
}

export type SeatMapResponse = {
  total_seats: number
  available_seats: number
  booked_seats: string[]
  available_seat_numbers: string[]
}

export type BookingRecord = {
  id: string
  schedule_id: number
  seat_number: string
  booking_status: string | null
  booking_date: string
}

export type CurrentBookingRecord = {
  id: string
  seat_number: string
  booking_status: string | null
  booking_date: string | null
  passenger_name: string
  bus_name: string
  departure_date: string | null
  departure_time: string | null
}

export type CurrentBookingList = CurrentBookingRecord[]

export type SearchFormState = {
  source: string
  destination: string
  journeyDate: string
}

export const initialSearchForm: SearchFormState = {
  source: '',
  destination: '',
  journeyDate: '',
}

export type SectionStatus = {
  type: 'idle' | 'loading' | 'success' | 'error'
  message: string
}

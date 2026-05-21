export type SectionStatus = {
  type: 'idle' | 'loading' | 'success' | 'error'
  message: string
}

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

export type JourneyFormState = {
  busId: string
  busName: string
  busNumber: string
  busType: string
  totalSeats: string
  operatorName: string
  amenities: string
  source: string
  destination: string
  distance: string
  duration: string
  departureTime: string
  arrivalTime: string
  journeyDate: string
  price: string
  availableSeats: string
  status: string
}

export const initialJourneyForm: JourneyFormState = {
  busId: '',
  busName: '',
  busNumber: '',
  busType: '',
  totalSeats: '40',
  operatorName: '',
  amenities: '',
  source: '',
  destination: '',
  distance: '',
  duration: '',
  departureTime: '',
  arrivalTime: '',
  journeyDate: '',
  price: '',
  availableSeats: '',
  status: 'active',
}
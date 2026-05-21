import type { RouteRecord, ScheduleRecord } from '../context/AdminDashboardTypes'

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

export async function fetchDashboardRecords(businessBase: string) {
  const [routeResponse, journeyResponse] = await Promise.all([
    requestJson(`${businessBase}/routes`, 'GET'),
    requestJson(`${businessBase}/schedules/details/all`, 'GET'),
  ])

  return {
    routes: routeResponse.ok ? (routeResponse.data as RouteRecord[]) : [],
    journeys: journeyResponse.ok ? (journeyResponse.data as ScheduleRecord[]) : [],
  }
}

export async function addDashboardEntity<T>(
  businessBase: string,
  entity: 'bus' | 'route' | 'schedule',
  data: unknown
) {
  const response = await requestJson(`${businessBase}/admin/add`, 'POST', { entity, data })
  return response.ok ? (response.data as T) : null
}

export async function updateDashboardEntity<T>(
  businessBase: string,
  entity: 'bus' | 'route' | 'schedule',
  id: number,
  data: unknown
) {
  const response = await requestJson(`${businessBase}/admin/update`, 'PUT', { entity, id, data })
  return response.ok ? (response.data as T) : null
}

export async function toggleDashboardScheduleStatus(
  businessBase: string,
  scheduleId: number,
  status: 'active' | 'inactive'
) {
  const response = await requestJson(`${businessBase}/admin/update`, 'PUT', {
    entity: 'schedule',
    id: scheduleId,
    data: { status },
  })

  return response.ok
}
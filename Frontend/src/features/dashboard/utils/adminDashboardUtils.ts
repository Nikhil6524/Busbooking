export function normalize(value: string) {
  return value.trim().toLowerCase()
}

export function getBusIds(journeys: Array<{ bus: { id: number } }>) {
  return Array.from(new Set(journeys.map((item) => item.bus.id))).sort((a, b) => a - b)
}
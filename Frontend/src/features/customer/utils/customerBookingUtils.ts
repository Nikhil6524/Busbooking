export function buildSeatRows(seats: string[]) {
  const rows: string[][] = []
  const groupSize = 4

  for (let index = 0; index < seats.length; index += groupSize) {
    rows.push(seats.slice(index, index + groupSize))
  }

  return rows
}

export function buildSeatLabels(totalSeats: number) {
  const letters = ['A', 'B', 'C', 'D']
  const seats: string[] = []

  for (let index = 0; index < totalSeats; index += 1) {
    const row = Math.floor(index / letters.length) + 1
    const letter = letters[index % letters.length]
    seats.push(`${row}${letter}`)
  }

  return seats
}

export function formatTime(value: string) {
  return value.replace('T', ' ')
}

export function formatDate(value: string) {
  return value.includes('T') ? value.split('T')[0] : value
}

export function isActiveSchedule(status: string | null) {
  return (status ?? '').trim().toLowerCase() === 'active'
}

function normalizeText(value: string) {
  return value.trim().toLowerCase()
}

function levenshtein(a: string, b: string) {
  const an = a.length
  const bn = b.length
  if (an === 0) return bn
  if (bn === 0) return an

  const matrix: number[][] = Array.from({ length: an + 1 }, () => Array(bn + 1).fill(0))
  for (let i = 0; i <= an; i += 1) matrix[i][0] = i
  for (let j = 0; j <= bn; j += 1) matrix[0][j] = j

  for (let i = 1; i <= an; i += 1) {
    for (let j = 1; j <= bn; j += 1) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      )
    }
  }

  return matrix[an][bn]
}

export function fuzzyMatch(text: string, query: string) {
  const t = normalizeText(text)
  const q = normalizeText(query)
  if (!q) return true
  if (t.includes(q)) return true

  const distance = levenshtein(t, q)
  // allow small typos: threshold proportional to query length
  const threshold = Math.max(1, Math.floor(q.length * 0.35))
  return distance <= threshold
}

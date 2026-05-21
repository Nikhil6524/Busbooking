type JwtPayload = {
  role?: string
}

function base64UrlToBase64(value: string) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/')
  const padding = normalized.length % 4
  if (padding === 0) {
    return normalized
  }

  return normalized + '='.repeat(4 - padding)
}

export function getRoleFromAccessToken(accessToken: string) {
  try {
    const parts = accessToken.split('.')
    if (parts.length !== 3) {
      return null
    }

    const payload = JSON.parse(
      atob(base64UrlToBase64(parts[1]))
    ) as JwtPayload

    return payload.role ?? null
  } catch {
    return null
  }
}

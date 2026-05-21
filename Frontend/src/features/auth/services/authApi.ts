export type AuthMode = 'login' | 'register'

export type RegisterPayload = {
  name: string
  email: string
  phone: string
  password: string
  role: string
}

export type LoginPayload = {
  email: string
  password: string
}

export type AuthResponse = {
  ok: boolean
  data: unknown
}

export type LoginResult = {
  access_token: string
  token_type: string
}

export async function submitAuth(
  baseUrl: string,
  mode: AuthMode,
  payload: RegisterPayload | LoginPayload
): Promise<AuthResponse> {
  const response = await fetch(`${baseUrl}/auth/${mode}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  })

  const contentType = response.headers.get('content-type') ?? ''
  const data = contentType.includes('application/json')
    ? await response.json()
    : await response.text()

  return {
    ok: response.ok,
    data,
  }
}

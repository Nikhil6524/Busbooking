import { useState } from 'react'

import { useAuthContext } from './useAuthContext'
import { getRoleFromAccessToken } from '../features/auth/utils/jwt'
import { submitAuth, type AuthMode, type LoginPayload, type RegisterPayload, type LoginResult } from '../features/auth/services/authApi'

type AuthStatus = {
  type: 'idle' | 'loading' | 'success' | 'error'
  message: string
  payload?: unknown
}

export function useAuth() {
  const { authBase, setRole, setAccessToken } = useAuthContext()
  const [status, setStatus] = useState<AuthStatus>({ type: 'idle', message: '' })

  const authenticate = async (mode: AuthMode, payload: RegisterPayload | LoginPayload) => {
    setStatus({ type: 'loading', message: 'Submitting...' })
    try {
      const response = await submitAuth(authBase, mode, payload)
      if (!response.ok) {
        setStatus({
          type: 'error',
          message: 'Invalid input.',
          payload: response.data,
        })
        return null
      }

      const authData = response.data as Partial<LoginResult>
      const role = typeof authData.access_token === 'string'
        ? getRoleFromAccessToken(authData.access_token)
        : null

      if (role) {
        setRole(role)
      }

      if (typeof authData.access_token === 'string') {
        setAccessToken(authData.access_token)
      }

      setStatus({
        type: 'success',
        message: mode === 'register' ? 'Account created.' : 'Login successful.',
      })

      return role
    } catch {
      setStatus({
        type: 'error',
        message: 'Invalid input.',
      })

      return null
    }
  }

  return {
    status,
    authenticate,
  }
}
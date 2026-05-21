import { useEffect, useMemo, useState } from 'react'

import { AuthContext, type AuthContextValue } from './authContext'

const STORAGE_KEY = 'busbook-role'
const TOKEN_KEY = 'busbook-token'

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const authBase = import.meta.env.VITE_AUTH_BASE ?? 'http://127.0.0.1:8001'
  const businessBase = import.meta.env.VITE_BUSINESS_BASE ?? 'http://127.0.0.1:8000'
  const [role, setRoleState] = useState<string | null>(() => window.localStorage.getItem(STORAGE_KEY))
  const [accessToken, setAccessTokenState] = useState<string | null>(() => window.localStorage.getItem(TOKEN_KEY))

  useEffect(() => {
    const savedRole = window.localStorage.getItem(STORAGE_KEY)
    const savedToken = window.localStorage.getItem(TOKEN_KEY)

    if (savedRole !== role) {
      setRoleState(savedRole)
    }

    if (savedToken !== accessToken) {
      setAccessTokenState(savedToken)
    }
  }, [accessToken, role])

  const value = useMemo<AuthContextValue>(() => ({
    authBase,
    businessBase,
    role,
    accessToken,
    setRole: (nextRole: string) => {
      window.localStorage.setItem(STORAGE_KEY, nextRole)
      setRoleState(nextRole)
    },
    setAccessToken: (nextToken: string) => {
      window.localStorage.setItem(TOKEN_KEY, nextToken)
      setAccessTokenState(nextToken)
    },
    clearSession: () => {
      window.localStorage.removeItem(STORAGE_KEY)
      window.localStorage.removeItem(TOKEN_KEY)
      setRoleState(null)
      setAccessTokenState(null)
    },
  }), [accessToken, authBase, businessBase, role])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
import { createContext } from 'react'

export type AuthContextValue = {
  authBase: string
  businessBase: string
  role: string | null
  accessToken: string | null
  setRole: (role: string) => void
  setAccessToken: (token: string) => void
  clearSession: () => void
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined)
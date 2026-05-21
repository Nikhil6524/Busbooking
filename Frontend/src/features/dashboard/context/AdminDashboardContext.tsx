import type { ReactNode } from 'react'
import { createContext, useContext } from 'react'

import { useAdminDashboard } from '../hooks/useAdminDashboard'

type AdminDashboardContextValue = ReturnType<typeof useAdminDashboard>

const AdminDashboardContext = createContext<AdminDashboardContextValue | null>(null)

type AdminDashboardProviderProps = {
  businessBase: string
  children: ReactNode
}

export function AdminDashboardProvider({ businessBase, children }: AdminDashboardProviderProps) {
  const dashboard = useAdminDashboard(businessBase)

  return <AdminDashboardContext.Provider value={dashboard}>{children}</AdminDashboardContext.Provider>
}

export function useAdminDashboardContext() {
  const context = useContext(AdminDashboardContext)

  if (!context) {
    throw new Error('useAdminDashboardContext must be used within AdminDashboardProvider')
  }

  return context
}
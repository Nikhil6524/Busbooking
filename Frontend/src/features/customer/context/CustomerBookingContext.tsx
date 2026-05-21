import type { ReactNode } from 'react'
import { createContext, useContext } from 'react'

import { useCustomerBooking } from '../hooks/useCustomerBooking'

type CustomerBookingContextValue = ReturnType<typeof useCustomerBooking>

const CustomerBookingContext = createContext<CustomerBookingContextValue | null>(null)

type CustomerBookingProviderProps = {
  businessBase: string
  children: ReactNode
}

export function CustomerBookingProvider({ businessBase, children }: CustomerBookingProviderProps) {
  const customerBooking = useCustomerBooking(businessBase)

  return <CustomerBookingContext.Provider value={customerBooking}>{children}</CustomerBookingContext.Provider>
}

export function useCustomerBookingContext() {
  const context = useContext(CustomerBookingContext)

  if (!context) {
    throw new Error('useCustomerBookingContext must be used within CustomerBookingProvider')
  }

  return context
}

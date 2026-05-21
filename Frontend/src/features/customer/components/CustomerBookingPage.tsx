import { useAuthContext } from '../../../hooks/useAuthContext'
import { CustomerBookingProvider } from '../context/CustomerBookingContext'
import { CustomerBookingHeader } from './CustomerBookingHeader'
import { CustomerSearchPanel } from './CustomerSearchPanel'
import { CustomerCurrentBooking } from './CustomerCurrentBooking'
import { CustomerAvailableBusesTable } from './CustomerAvailableBusesTable'
import { CustomerAvailableJourneysTable } from './CustomerAvailableJourneysTable'
import { CustomerSeatSelection } from './CustomerSeatSelection'
import { CustomerBookingHistory } from './CustomerBookingHistory'
import '../../../styles/customer.css'

export function CustomerBookingPage({ onLogout }: { onLogout: () => void }) {
  const { businessBase, clearSession, role } = useAuthContext()

  const handleLogout = () => {
    clearSession()
    onLogout()
  }

  if (role !== 'customer') {
    return (
      <div className="customer-shell denied">
        <div className="dashboard-card">
          <h1>Customer access only</h1>
          <p>You are not authorized to view this page.</p>
          <button type="button" className="ghost-button" onClick={handleLogout}>
            Back to login
          </button>
        </div>
      </div>
    )
  }

  return (
    <CustomerBookingProvider businessBase={businessBase}>
      <div className="customer-shell">
        <CustomerBookingHeader onLogout={handleLogout} />
        <CustomerCurrentBooking />
        <CustomerSearchPanel />
        <CustomerAvailableBusesTable />
        <CustomerAvailableJourneysTable />
        <CustomerSeatSelection />
        <CustomerBookingHistory />
      </div>
    </CustomerBookingProvider>
  )
}

import { useCustomerBookingContext } from '../context/CustomerBookingContext'

type CustomerBookingHeaderProps = {
  onLogout: () => void
}

export function CustomerBookingHeader({ onLogout }: CustomerBookingHeaderProps) {
  const { showCurrentBooking, showHistory, toggleCurrentBooking, toggleHistory } = useCustomerBookingContext()

  return (
    <header className="customer-header">
      <div>
        <span className="customer-kicker">BusBook</span>
        <h1>Find and book your next journey</h1>
        <p>Search by source, destination, and date, then pick a seat from the seat map.</p>
      </div>
      <div className="header-actions">
        <button type="button" className="ghost-button" onClick={() => void toggleCurrentBooking()}>
          {showCurrentBooking ? 'Hide current bookings' : 'Current bookings'}
        </button>
        <button type="button" className="ghost-button" onClick={() => void toggleHistory()}>
          {showHistory ? 'Hide history' : 'History'}
        </button>
        <button type="button" className="ghost-button" onClick={onLogout}>
          Logout
        </button>
      </div>
    </header>
  )
}

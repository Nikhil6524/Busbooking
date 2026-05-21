import { useCustomerBookingContext } from '../context/CustomerBookingContext'
import { formatDate, formatTime } from '../utils/customerBookingUtils'

export function CustomerCurrentBooking() {
  const { currentBookings, showCurrentBooking } = useCustomerBookingContext()

  if (!showCurrentBooking) {
    return null
  }

  return (
    <section className="table-card current-booking-card">
      <div className="section-head">
        <h2>My tickets</h2>
        <span>{currentBookings.length ? `${currentBookings.length} ticket(s)` : 'No active ticket'}</span>
      </div>

      {currentBookings.length ? (
        <div className="current-booking-list">
          {currentBookings.map((currentBooking) => (
            <article key={currentBooking.id} className="ticket-card">
              <div className="ticket-perforation ticket-perforation-top" />
              <div className="ticket-card-inner">
                <div className="ticket-topline">
                  <div>
                    <span className="ticket-label">Ticket for</span>
                    <strong>{currentBooking.passenger_name}</strong>
                  </div>
                  <div className="ticket-badge-group">
                    <span className="ticket-chip">Seat {currentBooking.seat_number}</span>
                    <span className="ticket-chip accent">{currentBooking.booking_status ?? 'confirmed'}</span>
                  </div>
                </div>

                <div className="ticket-main-grid">
                  <div>
                    <span>Bus</span>
                    <strong>{currentBooking.bus_name}</strong>
                  </div>
                  <div>
                    <span>Departure date</span>
                    <strong>{currentBooking.departure_date ? formatDate(currentBooking.departure_date) : '-'}</strong>
                  </div>
                  <div>
                    <span>Departure time</span>
                    <strong>{currentBooking.departure_time ? formatTime(currentBooking.departure_time) : '-'}</strong>
                  </div>
                  <div>
                    <span>Booking date</span>
                    <strong>{currentBooking.booking_date ? formatDate(currentBooking.booking_date) : '-'}</strong>
                  </div>
                  <div>
                    <span>Ticket ID</span>
                    <strong>{currentBooking.id}</strong>
                  </div>
                  <div>
                    <span>Status</span>
                    <strong>{currentBooking.booking_status ?? '-'}</strong>
                  </div>
                </div>

                <div className="ticket-footer">
                  <span>Show this ticket at boarding.</span>
                  <button type="button" className="ghost-button" onClick={() => window.print()}>
                    Print ticket
                  </button>
                </div>
              </div>
              <div className="ticket-perforation ticket-perforation-bottom" />
            </article>
          ))}
        </div>
      ) : (
        <div className="empty-state">No active ticket found.</div>
      )}
    </section>
  )
}
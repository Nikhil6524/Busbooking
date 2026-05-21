import { useCustomerBookingContext } from '../context/CustomerBookingContext'
import { formatTime } from '../utils/customerBookingUtils'

export function CustomerBookingHistory() {
  const { bookings, cancellingBookingId, cancelBooking, showHistory } = useCustomerBookingContext()

  if (!showHistory) {
    return null
  }

  return (
    <section className="table-card">
      <div className="section-head">
        <h2>My bookings</h2>
        <span>{bookings.length} booking(s)</span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>Schedule ID</th>
              <th>Seat</th>
              <th>Status</th>
              <th>Booked At</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map((booking) => {
              const isCancelled = (booking.booking_status ?? '').toLowerCase() === 'cancelled'

              return (
                <tr key={booking.id}>
                  <td>{booking.id}</td>
                  <td>{booking.schedule_id}</td>
                  <td>{booking.seat_number}</td>
                  <td>{booking.booking_status ?? '-'}</td>
                  <td>{formatTime(booking.booking_date)}</td>
                  <td>
                    <button
                      type="button"
                      className="secondary-button"
                      onClick={() => void cancelBooking(booking.id)}
                      disabled={isCancelled || cancellingBookingId === booking.id}
                    >
                      {isCancelled
                        ? 'Cancelled'
                        : cancellingBookingId === booking.id
                          ? 'Cancelling...'
                          : 'Cancel booking'}
                    </button>
                  </td>
                </tr>
              )
            })}
            {!bookings.length && (
              <tr>
                <td colSpan={6} className="empty-state">No bookings found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}

import { useCustomerBookingContext } from '../context/CustomerBookingContext'
import { buildSeatLabels, buildSeatRows, formatTime } from '../utils/customerBookingUtils'

export function CustomerSeatSelection() {
  const {
    bookingStatus,
    bookSeat,
    selectedBusLabel,
    selectedSchedule,
    selectedSeat,
    seatSectionRef,
    seatMap,
    setSelectedSeat,
  } = useCustomerBookingContext()

  return (
    <section className="seat-layout-card" ref={seatSectionRef}>
      <div className="section-head">
        <h2>Seat selection</h2>
        <span>{selectedSchedule ? `Bus ${selectedSchedule.bus.id}` : 'No journey selected'}</span>
      </div>

      {selectedSchedule ? (
        <>
          <div className="journey-summary">
            <div>
              <strong>{selectedBusLabel}</strong>
              <p>{selectedSchedule.route.source} to {selectedSchedule.route.destination}</p>
            </div>
            <div>
              <strong>{selectedSchedule.schedule.journey_date}</strong>
              <p>{formatTime(selectedSchedule.schedule.departure_time)} - {formatTime(selectedSchedule.schedule.arrival_time)}</p>
            </div>
          </div>

          {seatMap ? (
            <>
              <div className="seat-meta">
                <span>Total seats: {seatMap.total_seats}</span>
                <span>Available: {seatMap.available_seats}</span>
                <span>Booked: {seatMap.booked_seats.length}</span>
              </div>

              <div className="seat-grid">
                {buildSeatRows(buildSeatLabels(seatMap.total_seats)).map((row, index) => (
                  <div key={`${index}-${row.join('-')}`} className="seat-row">
                    {row.map((seat) => (
                      <button
                        key={seat}
                        type="button"
                        className={`seat ${selectedSeat === seat ? 'selected' : ''} ${seatMap.booked_seats.includes(seat) ? 'booked' : ''}`}
                        onClick={() => {
                          if (!seatMap.booked_seats.includes(seat)) {
                            setSelectedSeat(seat)
                          }
                        }}
                        disabled={seatMap.booked_seats.includes(seat)}
                      >
                        {seat}
                      </button>
                    ))}
                  </div>
                ))}
              </div>

              <div className="booking-row">
                <div className="selected-seat-pill">Selected seat: {selectedSeat || '-'}</div>
                <button type="button" className="primary-button" onClick={() => void bookSeat()}>
                  Book seat
                </button>
              </div>

              {bookingStatus.message && <div className={`banner ${bookingStatus.type}`}>{bookingStatus.message}</div>}
            </>
          ) : (
            <div className="placeholder">Click “Select seat” on a journey to load the seat map.</div>
          )}
        </>
      ) : (
        <div className="placeholder">Choose a search result to start booking.</div>
      )}
    </section>
  )
}

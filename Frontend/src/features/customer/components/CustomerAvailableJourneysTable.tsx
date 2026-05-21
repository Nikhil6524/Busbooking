import { useCustomerBookingContext } from '../context/CustomerBookingContext'
import { formatTime } from '../utils/customerBookingUtils'

export function CustomerAvailableJourneysTable() {
  const { loadSeatMap, loading, results } = useCustomerBookingContext()

  return (
    <section className="table-card">
      <div className="section-head">
        <h2>Available journeys</h2>
        <span>{loading ? 'Searching...' : `${results.length} result(s)`}</span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Bus</th>
              <th>Route</th>
              <th>Date</th>
              <th>Departure</th>
              <th>Arrival</th>
              <th>Price</th>
              <th>Seats</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {results.map((record) => (
              <tr key={record.schedule.id}>
                <td>
                  <strong>{record.bus.bus_name}</strong>
                  <div className="muted">{record.bus.bus_number}</div>
                </td>
                <td>{record.route.source} to {record.route.destination}</td>
                <td>{record.schedule.journey_date}</td>
                <td>{formatTime(record.schedule.departure_time)}</td>
                <td>{formatTime(record.schedule.arrival_time)}</td>
                <td>{record.schedule.price}</td>
                <td>{record.schedule.available_seats}</td>
                <td>
                  <button type="button" className="secondary-button" onClick={() => void loadSeatMap(record)}>
                    Select seat
                  </button>
                </td>
              </tr>
            ))}
            {!results.length && (
              <tr>
                <td colSpan={8} className="empty-state">Search for a journey to see available buses.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}

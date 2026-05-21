import { useCustomerBookingContext } from '../context/CustomerBookingContext'
import { formatTime } from '../utils/customerBookingUtils'

export function CustomerAvailableBusesTable() {
  const { buses, loadSeatMap, favorites, toggleFavorite } = useCustomerBookingContext()

  return (
    <section className="table-card">
      <div className="section-head">
        <h2>All available buses</h2>
        <span>{buses.length} buses</span>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Number</th>
              <th>Source</th>
              <th>Destination</th>
              <th>Date</th>
              <th>Departure</th>
              <th>Arrival</th>
              <th>Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {buses.map((record) => (
              <tr key={record.schedule.id}>
                <td>
                  <strong>{record.bus.bus_name}</strong>
                  <button
                    type="button"
                    aria-label={favorites.includes(record.bus.id) ? 'Unfavorite' : 'Favorite'}
                    className="favorite-button"
                    onClick={() => void toggleFavorite(record.bus.id)}
                    style={{ marginLeft: 8 }}
                  >
                    {favorites.includes(record.bus.id) ? '★' : '☆'}
                  </button>
                </td>
                <td>{record.bus.bus_number}</td>
                <td>{record.route.source}</td>
                <td>{record.route.destination}</td>
                <td>{record.schedule.journey_date}</td>
                <td>{formatTime(record.schedule.departure_time)}</td>
                <td>{formatTime(record.schedule.arrival_time)}</td>
                <td>{record.schedule.price}</td>
                <td>
                  <button type="button" className="secondary-button" onClick={() => void loadSeatMap(record)}>
                    Book this bus
                  </button>
                </td>
              </tr>
            ))}
            {!buses.length && (
              <tr>
                <td colSpan={9} className="empty-state">No buses available yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}

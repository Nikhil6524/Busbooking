import { useAdminDashboardContext } from '../context/AdminDashboardContext'
import { normalize } from '../utils/adminDashboardUtils'

export function AdminJourneyRecordsTable() {
  const { busIds, journeys, loading, toggleScheduleStatus, updatingScheduleId, setForm, setEditingBusId } = useAdminDashboardContext()

  return (
    <section className="dashboard-card">
      <div className="editor-head">
        <h2>Journey Records Table</h2>
        <span className="record-chip">Bus IDs: {busIds.length ? busIds.join(', ') : '-'}</span>
      </div>

      <div className="table-wrap">
        <table className="records-table">
          <thead>
            <tr>
              <th>Bus ID</th>
              <th>Bus</th>
              <th>Route</th>
              <th>Date</th>
              <th>Departure</th>
              <th>Arrival</th>
              <th>Price</th>
              <th>Seats</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {journeys.map((item) => (
              <tr key={item.schedule.id}>
                <td>{item.bus.id}</td>
                <td>{item.bus.bus_name} ({item.bus.bus_number})</td>
                <td>{item.route.source} to {item.route.destination}</td>
                <td>{item.schedule.journey_date}</td>
                <td>{item.schedule.departure_time}</td>
                <td>{item.schedule.arrival_time}</td>
                <td>{item.schedule.price}</td>
                <td>{item.schedule.available_seats}</td>
                <td>
                  <div className="status-cell">
                    <span className={`status-pill ${normalize(item.schedule.status ?? '') || 'unknown'}`}>
                      {item.schedule.status ?? 'inactive'}
                    </span>
                    <button
                      type="button"
                      className="status-toggle"
                      onClick={() => void toggleScheduleStatus(item.schedule)}
                      disabled={updatingScheduleId === item.schedule.id || loading}
                    >
                      {updatingScheduleId === item.schedule.id
                        ? 'Updating...'
                        : normalize(item.schedule.status ?? '') === 'active'
                          ? 'Set inactive'
                          : 'Set active'}
                    </button>
                  </div>
                </td>
                <td>
                  <div className="row-actions">
                    <button
                      type="button"
                      className="secondary small-icon"
                      title={`Edit bus ${item.bus.id}`}
                      onClick={() => {
                        setForm((prev) => ({
                          ...prev,
                          busId: String(item.bus.id),
                          busName: item.bus.bus_name ?? '',
                          busNumber: item.bus.bus_number ?? '',
                          busType: item.bus.bus_type ?? '',
                          totalSeats: String(item.bus.total_seats ?? ''),
                          operatorName: item.bus.operator_name ?? '',
                          amenities: item.bus.amenities ?? '',
                          source: item.route.source ?? '',
                          destination: item.route.destination ?? '',
                          distance: item.route.distance ? String(item.route.distance) : '',
                          duration: item.route.duration ?? '',
                          departureTime: item.schedule.departure_time ?? '',
                          arrivalTime: item.schedule.arrival_time ?? '',
                          journeyDate: item.schedule.journey_date ?? '',
                          price: String(item.schedule.price ?? ''),
                          availableSeats: String(item.schedule.available_seats ?? ''),
                          status: item.schedule.status ?? '',
                        }))
                        setEditingBusId(item.bus.id)
                        // scroll to top where the form lives
                        const el = document.querySelector('.editor-card')
                        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
                      }}
                    >
                      +
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {!journeys.length && (
              <tr>
                <td colSpan={10} className="empty">
                  No records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}
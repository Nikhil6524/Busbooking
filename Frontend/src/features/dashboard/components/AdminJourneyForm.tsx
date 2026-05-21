import { useAdminDashboardContext } from '../context/AdminDashboardContext'

export function AdminJourneyForm() {
  const { form, loading, setForm, status, submitJourneyEntity } = useAdminDashboardContext()
  const { editingBusId } = useAdminDashboardContext()

  return (
    <section className="dashboard-card editor-card">
      <div className="editor-head">
        <h2>{editingBusId ? `Editing Bus ${editingBusId}` : 'Combined Journey Entity'}</h2>
        <span className="record-chip">{loading ? 'Refreshing...' : editingBusId ? 'Editing' : 'Journey editor'}</span>
      </div>

      <form
        className="entity-grid"
        onSubmit={(event) => {
          event.preventDefault()
          void submitJourneyEntity()
        }}
      >
        <label>
          Bus ID
          <input
            type="number"
            value={form.busId}
            onChange={(event) => setForm((prev) => ({ ...prev, busId: event.target.value }))}
            placeholder="Required"
          />
        </label>
        <label>
          Bus Name
          <input
            value={form.busName}
            onChange={(event) => setForm((prev) => ({ ...prev, busName: event.target.value }))}
            placeholder="Blue Star"
          />
        </label>
        <label>
          Bus Number
          <input
            value={form.busNumber}
            onChange={(event) => setForm((prev) => ({ ...prev, busNumber: event.target.value }))}
            placeholder="TN 09 BR 7788"
          />
        </label>
        <label>
          Bus Type
          <input
            value={form.busType}
            onChange={(event) => setForm((prev) => ({ ...prev, busType: event.target.value }))}
            placeholder="AC Sleeper"
          />
        </label>
        <label>
          Total Seats
          <input
            type="number"
            value={form.totalSeats}
            onChange={(event) => setForm((prev) => ({ ...prev, totalSeats: event.target.value }))}
          />
        </label>
        <label>
          Operator Name
          <input
            value={form.operatorName}
            onChange={(event) => setForm((prev) => ({ ...prev, operatorName: event.target.value }))}
            placeholder="Transit Co"
          />
        </label>
        <label className="wide">
          Amenities
          <input
            value={form.amenities}
            onChange={(event) => setForm((prev) => ({ ...prev, amenities: event.target.value }))}
            placeholder="WiFi, USB charging"
          />
        </label>

        <label>
          Source
          <input
            value={form.source}
            onChange={(event) => setForm((prev) => ({ ...prev, source: event.target.value }))}
            placeholder="Chennai"
          />
        </label>
        <label>
          Destination
          <input
            value={form.destination}
            onChange={(event) => setForm((prev) => ({ ...prev, destination: event.target.value }))}
            placeholder="Bangalore"
          />
        </label>
        <label>
          Distance
          <input
            type="number"
            value={form.distance}
            onChange={(event) => setForm((prev) => ({ ...prev, distance: event.target.value }))}
            placeholder="345"
          />
        </label>
        <label>
          Duration
          <input
            value={form.duration}
            onChange={(event) => setForm((prev) => ({ ...prev, duration: event.target.value }))}
            placeholder="6h"
          />
        </label>

        <label>
          Departure
          <input
            value={form.departureTime}
            onChange={(event) => setForm((prev) => ({ ...prev, departureTime: event.target.value }))}
            placeholder="2026-05-20T10:00:00"
          />
        </label>
        <label>
          Arrival
          <input
            value={form.arrivalTime}
            onChange={(event) => setForm((prev) => ({ ...prev, arrivalTime: event.target.value }))}
            placeholder="2026-05-20T16:00:00"
          />
        </label>
        <label>
          Journey Date
          <input
            type="date"
            value={form.journeyDate}
            onChange={(event) => setForm((prev) => ({ ...prev, journeyDate: event.target.value }))}
          />
        </label>
        <label>
          Price
          <input
            type="number"
            value={form.price}
            onChange={(event) => setForm((prev) => ({ ...prev, price: event.target.value }))}
            placeholder="750"
          />
        </label>
        <label>
          Available Seats
          <input
            type="number"
            value={form.availableSeats}
            onChange={(event) => setForm((prev) => ({ ...prev, availableSeats: event.target.value }))}
            placeholder="38"
          />
        </label>
        <label>
          Status
          <input
            value={form.status}
            onChange={(event) => setForm((prev) => ({ ...prev, status: event.target.value }))}
            placeholder="active"
          />
        </label>

        <div className="wide actions">
          <button type="submit" className="primary">
            {editingBusId ? 'Update' : 'Save Combined Entity'}
          </button>
        </div>
      </form>

      {status.message && (
        <div className={`status ${status.type}`}>
          <strong>{status.message}</strong>
        </div>
      )}
    </section>
  )
}
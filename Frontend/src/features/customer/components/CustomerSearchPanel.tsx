import { useCustomerBookingContext } from '../context/CustomerBookingContext'

export function CustomerSearchPanel() {
  const { loadSearchResults, searchForm, setSearchForm, status } = useCustomerBookingContext()

  return (
    <section className="hero-card">
      <form
        className="search-grid"
        onSubmit={(event) => {
          event.preventDefault()
          void loadSearchResults()
        }}
      >
        <label>
          Source
          <input
            value={searchForm.source}
            onChange={(event) => setSearchForm((prev) => ({ ...prev, source: event.target.value }))}
            placeholder="Chennai"
          />
        </label>
        <label>
          Destination
          <input
            value={searchForm.destination}
            onChange={(event) => setSearchForm((prev) => ({ ...prev, destination: event.target.value }))}
            placeholder="Bangalore"
          />
        </label>
        <label>
          Journey Date
          <input
            type="date"
            value={searchForm.journeyDate}
            onChange={(event) => setSearchForm((prev) => ({ ...prev, journeyDate: event.target.value }))}
          />
        </label>
        <div className="search-actions">
          <button type="submit" className="primary-button">Search journeys</button>
        </div>
      </form>

      {status.message && <div className={`banner ${status.type}`}>{status.message}</div>}
    </section>
  )
}

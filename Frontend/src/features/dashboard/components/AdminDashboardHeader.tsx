type AdminDashboardHeaderProps = {
  onLogout: () => void
}

export function AdminDashboardHeader({ onLogout }: AdminDashboardHeaderProps) {
  return (
    <header className="dashboard-header">
      <div>
        <span className="dashboard-kicker">BusBook Admin</span>
        <h1>Journey Entity Studio</h1>
        <p>Manage bus, route, and schedule together using one user-given bus ID.</p>
      </div>
      <button type="button" className="secondary" onClick={onLogout}>
        Logout
      </button>
    </header>
  )
}
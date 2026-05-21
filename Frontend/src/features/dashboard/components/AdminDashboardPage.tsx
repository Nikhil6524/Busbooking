import { useAuthContext } from '../../../hooks/useAuthContext'
import { AdminDashboardProvider } from '../context/AdminDashboardContext'
import { AdminDashboardHeader } from './AdminDashboardHeader'
import { AdminJourneyForm } from './AdminJourneyForm'
import { AdminJourneyRecordsTable } from './AdminJourneyRecordsTable'
import '../../../styles/dashboard.css'

export function AdminDashboardPage({ onLogout }: { onLogout: () => void }) {
  const { businessBase, role, clearSession } = useAuthContext()

  const handleLogout = () => {
    clearSession()
    onLogout()
  }

  if (role !== 'admin') {
    return (
      <div className="dashboard-shell denied">
        <div className="dashboard-card">
          <h1>Admin access only</h1>
          <p>You are not authorized to view this page.</p>
          <button type="button" className="secondary" onClick={handleLogout}>
            Back to login
          </button>
        </div>
      </div>
    )
  }

  return (
    <AdminDashboardProvider businessBase={businessBase}>
      <div className="dashboard-shell">
        <AdminDashboardHeader onLogout={handleLogout} />
        <AdminJourneyForm />
        <AdminJourneyRecordsTable />
      </div>
    </AdminDashboardProvider>
  )
}

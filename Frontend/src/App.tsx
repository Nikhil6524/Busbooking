import { useEffect, useState } from 'react'

import { AuthPage } from './features/auth/components/AuthPage'
import { AuthProvider } from './context/AuthProvider'
import { useAuthContext } from './hooks/useAuthContext'
import { AdminDashboardPage } from './features/dashboard/components/AdminDashboardPage'
import { CustomerBookingPage } from './features/customer/components/CustomerBookingPage'

function App() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  )
}

function AppRouter() {
  const { role, clearSession } = useAuthContext()
  const [path, setPath] = useState(window.location.pathname)

  useEffect(() => {
    const handlePopState = () => setPath(window.location.pathname)
    window.addEventListener('popstate', handlePopState)

    return () => window.removeEventListener('popstate', handlePopState)
  }, [])

  const navigate = (nextPath: string) => {
    window.history.pushState({}, '', nextPath)
    setPath(nextPath)
  }

  const handleAuthenticated = (loggedRole: string | null) => {
    if (loggedRole === 'admin') {
      navigate('/admin')
      return
    }

    if (loggedRole === 'customer') {
      navigate('/')
    }
  }

  const handleLogout = () => {
    clearSession()
    navigate('/')
  }

  if (path.startsWith('/admin')) {
    return <AdminDashboardPage onLogout={handleLogout} />
  }

  if (role === 'customer') {
    return <CustomerBookingPage onLogout={handleLogout} />
  }

  return <AuthPage onAuthenticated={handleAuthenticated} />
}

export default App


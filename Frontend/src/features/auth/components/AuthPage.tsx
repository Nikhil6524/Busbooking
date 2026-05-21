import { useState } from 'react'

import { useAuth } from '../../../hooks/useAuth'
import type { AuthMode } from '../services/authApi'
import './AuthPage.css'

type AuthFormState = {
  name: string
  email: string
  phone: string
  password: string
  role: string
}

const initialForm: AuthFormState = {
  name: '',
  email: '',
  phone: '',
  password: '',
  role: 'customer',
}

type AuthPageProps = {
  onAuthenticated?: (role: string | null) => void
}

export function AuthPage({ onAuthenticated }: AuthPageProps) {
  const [mode, setMode] = useState<AuthMode>('login')
  const [form, setForm] = useState<AuthFormState>(initialForm)
  const { status, authenticate } = useAuth()

  const isRegister = mode === 'register'

  const handleChange = (key: keyof AuthFormState) =>
    (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      setForm((prev) => ({ ...prev, [key]: event.target.value }))
    }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()

    const payload = isRegister
      ? {
          name: form.name,
          email: form.email,
          phone: form.phone,
          password: form.password,
          role: form.role,
        }
      : {
          email: form.email,
          password: form.password,
        }

    const role = await authenticate(mode, payload)

    if (onAuthenticated) {
      onAuthenticated(role)
    }
  }

  return (
    <div className="auth-shell">
      <section className="auth-visual card">
        <div className="brand">
          <span className="brand-pill">BusBook</span>
          <h2>Travel booking with fewer clicks and cleaner tickets.</h2>
          <p>
            Search routes, star your favorite buses, and keep your current ticket visible after every booking.
          </p>
        </div>

        <div className="route-card">
          <h3>Today’s quick route</h3>
          <div className="route-line">
            <span>A</span>
            <span className="route-dash" />
            <span>B</span>
          </div>
          <div className="route-meta">
            <span>Live seats</span>
            <span>Fast booking</span>
            <span>Ticket view</span>
          </div>
        </div>

        <div className="stats">
          <article>
            <h4>24/7</h4>
            <p>booking access</p>
          </article>
          <article>
            <h4>1 tap</h4>
            <p>seat selection</p>
          </article>
          <article>
            <h4>Live</h4>
            <p>current ticket</p>
          </article>
        </div>
      </section>

      <section className="auth-panel">
        <header className="auth-header">
          <h1>{isRegister ? 'Create your account' : 'Welcome back'}</h1>
          <p>
            {isRegister
              ? 'Set up your profile and start booking seats.'
              : 'Log in to manage your bookings and favorites.'}
          </p>
        </header>

        <div className="mode-toggle" role="tablist">
          <button
            type="button"
            className={mode === 'login' ? 'active' : ''}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={mode === 'register' ? 'active' : ''}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          {isRegister && (
            <label>
              Full name
              <input
                type="text"
                value={form.name}
                onChange={handleChange('name')}
                placeholder="Asha Kumar"
                required
              />
            </label>
          )}

          <label>
            Email
            <input
              type="email"
              value={form.email}
              onChange={handleChange('email')}
              placeholder="you@busbook.in"
              required
            />
          </label>

          {isRegister && (
            <label>
              Phone
              <input
                type="tel"
                value={form.phone}
                onChange={handleChange('phone')}
                placeholder="9876543210"
                required
              />
            </label>
          )}

          <label>
            Password
            <input
              type="password"
              value={form.password}
              onChange={handleChange('password')}
              placeholder="••••••••"
              required
            />
          </label>

          {isRegister && (
            <label>
              Role
              <select value={form.role} onChange={handleChange('role')}>
                <option value="customer">Customer</option>
                <option value="admin">Admin</option>
              </select>
            </label>
          )}

          <button type="submit" className="primary" disabled={status.type === 'loading'}>
            {status.type === 'loading'
              ? 'Submitting...'
              : isRegister
                ? 'Create account'
                : 'Login'}
          </button>
        </form>

        {status.message && (
          <div className={`status ${status.type}`}>
            <strong>{status.message}</strong>
          </div>
        )}

        <div className="auth-note card">
          <strong>New here?</strong>
          <p>Register as a customer to book seats or as an admin to manage buses and schedules.</p>
        </div>

        <footer className="auth-footer">
          <span>Need help?</span>
          <a href="mailto:support@busbook.in">support@busbook.in</a>
        </footer>
      </section>
    </div>
  )
}

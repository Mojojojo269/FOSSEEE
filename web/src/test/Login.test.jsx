import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import Login from '../components/Login'
import { AuthProvider } from '../context/AuthContext'
import * as api from '../services/api'

// Mock the API
vi.mock('../services/api', () => ({
  authAPI: {
    login: vi.fn()
  }
}))

// Mock useNavigate
const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate
  }
})

describe('Login Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders login form', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    )

    expect(screen.getByText(/Chemical Equipment Parameter Visualizer/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Login/i })).toBeInTheDocument()
  })

  it('shows error when fields are empty', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    )

    const loginButton = screen.getByRole('button', { name: /Login/i })
    fireEvent.click(loginButton)

    // Form validation should prevent submission
    expect(api.authAPI.login).not.toHaveBeenCalled()
  })

  it('calls login API with credentials', async () => {
    api.authAPI.login.mockResolvedValue({
      data: {
        token: 'test-token',
        user_id: 1,
        username: 'testuser'
      }
    })

    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    )

    const usernameInput = screen.getByLabelText(/Username/i)
    const passwordInput = screen.getByLabelText(/Password/i)
    const loginButton = screen.getByRole('button', { name: /Login/i })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'testpass123' } })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(api.authAPI.login).toHaveBeenCalledWith('testuser', 'testpass123')
    })
  })

  it('displays error message on login failure', async () => {
    api.authAPI.login.mockRejectedValue({
      response: {
        data: {
          error: 'Invalid credentials'
        }
      }
    })

    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    )

    const usernameInput = screen.getByLabelText(/Username/i)
    const passwordInput = screen.getByLabelText(/Password/i)
    const loginButton = screen.getByRole('button', { name: /Login/i })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'wrongpass' } })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument()
    })
  })
})

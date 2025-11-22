import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'
import * as api from '../services/api'

// Mock the API
vi.mock('../services/api', () => ({
  authAPI: {
    login: vi.fn()
  },
  datasetAPI: {
    upload: vi.fn(),
    getHistory: vi.fn(),
    getSummary: vi.fn(),
    downloadPDF: vi.fn()
  }
}))

describe('Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
  })

  it('login flow with AuthContext', async () => {
    api.authAPI.login.mockResolvedValue({
      data: {
        token: 'test-token',
        user_id: 1,
        username: 'testuser'
      }
    })

    render(<App />)

    // Should show login page initially
    expect(screen.getByText(/Chemical Equipment Parameter Visualizer/i)).toBeInTheDocument()

    const usernameInput = screen.getByLabelText(/Username/i)
    const passwordInput = screen.getByLabelText(/Password/i)
    const loginButton = screen.getByRole('button', { name: /Login/i })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'testpass123' } })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(api.authAPI.login).toHaveBeenCalledWith('testuser', 'testpass123')
    })

    // Token should be stored in localStorage
    await waitFor(() => {
      expect(localStorage.getItem('token')).toBe('test-token')
      expect(localStorage.getItem('username')).toBe('testuser')
    })
  })

  it('redirects to upload page after successful login', async () => {
    api.authAPI.login.mockResolvedValue({
      data: {
        token: 'test-token',
        user_id: 1,
        username: 'testuser'
      }
    })

    render(<App />)

    const usernameInput = screen.getByLabelText(/Username/i)
    const passwordInput = screen.getByLabelText(/Password/i)
    const loginButton = screen.getByRole('button', { name: /Login/i })

    fireEvent.change(usernameInput, { target: { value: 'testuser' } })
    fireEvent.change(passwordInput, { target: { value: 'testpass123' } })
    fireEvent.click(loginButton)

    await waitFor(() => {
      expect(screen.getByText(/Upload CSV File/i)).toBeInTheDocument()
    })
  })

  it('navigation between pages works', async () => {
    // Set up authenticated state
    localStorage.setItem('token', 'test-token')
    localStorage.setItem('username', 'testuser')

    api.datasetAPI.getHistory.mockResolvedValue({
      data: {
        datasets: []
      }
    })

    render(<App />)

    // Should be on upload page
    await waitFor(() => {
      expect(screen.getByText(/Upload CSV File/i)).toBeInTheDocument()
    })

    // Navigate to history
    const historyLink = screen.getByText('History')
    fireEvent.click(historyLink)

    await waitFor(() => {
      expect(screen.getByText(/Upload History/i)).toBeInTheDocument()
    })
  })
})

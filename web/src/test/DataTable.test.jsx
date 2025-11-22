import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import DataTable from '../components/DataTable'

describe('DataTable Component', () => {
  const mockData = [
    {
      'Equipment Name': 'Pump-A1',
      'Type': 'Pump',
      'Flowrate': 150.5,
      'Pressure': 45.2,
      'Temperature': 85.3
    },
    {
      'Equipment Name': 'Reactor-R1',
      'Type': 'Reactor',
      'Flowrate': 200.0,
      'Pressure': 120.5,
      'Temperature': 350.0
    }
  ]

  it('renders table with data', () => {
    render(<DataTable data={mockData} />)

    expect(screen.getByText('Equipment Data')).toBeInTheDocument()
    expect(screen.getByText('Pump-A1')).toBeInTheDocument()
    expect(screen.getByText('Reactor-R1')).toBeInTheDocument()
    expect(screen.getByText('Pump')).toBeInTheDocument()
    expect(screen.getByText('Reactor')).toBeInTheDocument()
  })

  it('renders all column headers', () => {
    render(<DataTable data={mockData} />)

    expect(screen.getByText('Equipment Name')).toBeInTheDocument()
    expect(screen.getByText('Type')).toBeInTheDocument()
    expect(screen.getByText('Flowrate')).toBeInTheDocument()
    expect(screen.getByText('Pressure')).toBeInTheDocument()
    expect(screen.getByText('Temperature')).toBeInTheDocument()
  })

  it('displays no data message when data is empty', () => {
    render(<DataTable data={[]} />)

    expect(screen.getByText('No data available')).toBeInTheDocument()
  })

  it('displays no data message when data is null', () => {
    render(<DataTable data={null} />)

    expect(screen.getByText('No data available')).toBeInTheDocument()
  })

  it('renders correct number of rows', () => {
    const { container } = render(<DataTable data={mockData} />)
    const rows = container.querySelectorAll('tbody tr')
    expect(rows.length).toBe(2)
  })
})

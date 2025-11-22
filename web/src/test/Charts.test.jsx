import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import PieChart from '../components/PieChart'
import BarChart from '../components/BarChart'

// Mock Chart.js
vi.mock('react-chartjs-2', () => ({
  Pie: () => <div data-testid="pie-chart">Pie Chart</div>,
  Bar: () => <div data-testid="bar-chart">Bar Chart</div>
}))

describe('Chart Components', () => {
  const mockTypeDistribution = {
    'Pump': 4,
    'Reactor': 2,
    'Heat Exchanger': 2
  }

  const mockSummary = {
    avg_flowrate: 173.13,
    avg_pressure: 62.04,
    avg_temperature: 143.79
  }

  describe('PieChart', () => {
    it('renders pie chart', () => {
      const { getByTestId } = render(<PieChart data={mockTypeDistribution} />)
      expect(getByTestId('pie-chart')).toBeInTheDocument()
    })
  })

  describe('BarChart', () => {
    it('renders bar chart', () => {
      const { getByTestId } = render(<BarChart summary={mockSummary} />)
      expect(getByTestId('bar-chart')).toBeInTheDocument()
    })
  })
})

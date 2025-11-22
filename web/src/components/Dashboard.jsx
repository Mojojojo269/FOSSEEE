import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DataTable from './DataTable';
import PieChart from './PieChart';
import BarChart from './BarChart';
import { datasetAPI } from '../services/api';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    // Get dataset from sessionStorage
    const storedDataset = sessionStorage.getItem('currentDataset');
    if (storedDataset) {
      setDataset(JSON.parse(storedDataset));
    } else {
      // If no dataset, redirect to upload
      navigate('/upload');
    }
  }, [navigate]);

  const handleDownloadPDF = async () => {
    if (!dataset) return;

    setLoading(true);
    setError('');

    try {
      const response = await datasetAPI.downloadPDF(dataset.dataset_id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${dataset.filename}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download PDF. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!dataset) {
    return <div className="loading">Loading...</div>;
  }

  const { data, summary, filename, timestamp } = dataset;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <button onClick={handleDownloadPDF} disabled={loading} className="pdf-button">
          {loading ? 'Generating PDF...' : 'Download PDF Report'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="dataset-info">
        <p><strong>Filename:</strong> {filename}</p>
        <p><strong>Upload Time:</strong> {new Date(timestamp).toLocaleString()}</p>
      </div>

      <div className="summary-cards">
        <div className="summary-card">
          <h3>Total Equipment</h3>
          <p className="summary-value">{summary.total_count}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Flowrate</h3>
          <p className="summary-value">{summary.avg_flowrate.toFixed(2)}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Pressure</h3>
          <p className="summary-value">{summary.avg_pressure.toFixed(2)}</p>
        </div>
        <div className="summary-card">
          <h3>Avg Temperature</h3>
          <p className="summary-value">{summary.avg_temperature.toFixed(2)}</p>
        </div>
      </div>

      <DataTable data={data} />

      <div className="charts-container">
        <div className="chart-box">
          <PieChart data={summary.type_distribution} />
        </div>
        <div className="chart-box">
          <BarChart summary={summary} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

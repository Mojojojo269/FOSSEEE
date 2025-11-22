import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { datasetAPI } from '../services/api';
import '../styles/HistoryPage.css';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await datasetAPI.getHistory();
      setHistory(response.data.datasets);
    } catch (err) {
      setError('Failed to load history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewDataset = (dataset) => {
    // Store dataset in sessionStorage and navigate to dashboard
    const datasetWithData = {
      dataset_id: dataset.id,
      filename: dataset.filename,
      timestamp: dataset.timestamp,
      summary: dataset.summary,
      data: [] // We don't have the full data, but dashboard can handle it
    };
    sessionStorage.setItem('currentDataset', JSON.stringify(datasetWithData));
    navigate('/dashboard');
  };

  if (loading) {
    return (
      <div className="history-container">
        <div className="loading">Loading history...</div>
      </div>
    );
  }

  return (
    <div className="history-container">
      <h1>Upload History</h1>
      <p className="history-description">Last 5 dataset uploads</p>

      {error && <div className="error-message">{error}</div>}

      {history.length === 0 ? (
        <div className="no-history">
          <p>No upload history available</p>
          <button onClick={() => navigate('/upload')}>Upload Your First Dataset</button>
        </div>
      ) : (
        <div className="history-list">
          {history.map((dataset) => (
            <div key={dataset.id} className="history-item">
              <div className="history-item-header">
                <h3>{dataset.filename}</h3>
                <span className="history-date">
                  {new Date(dataset.timestamp).toLocaleString()}
                </span>
              </div>
              <div className="history-summary">
                <div className="summary-item">
                  <span className="label">Total Equipment:</span>
                  <span className="value">{dataset.summary.total_count}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Avg Flowrate:</span>
                  <span className="value">{dataset.summary.avg_flowrate.toFixed(2)}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Avg Pressure:</span>
                  <span className="value">{dataset.summary.avg_pressure.toFixed(2)}</span>
                </div>
                <div className="summary-item">
                  <span className="label">Avg Temperature:</span>
                  <span className="value">{dataset.summary.avg_temperature.toFixed(2)}</span>
                </div>
              </div>
              <div className="history-types">
                <strong>Equipment Types:</strong>
                {Object.entries(dataset.summary.type_distribution).map(([type, count]) => (
                  <span key={type} className="type-badge">
                    {type}: {count}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default HistoryPage;

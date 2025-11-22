import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { datasetAPI } from '../services/api';
import '../styles/UploadPage.css';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.csv')) {
        setError('Please select a CSV file');
        setFile(null);
        return;
      }
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        setFile(null);
        return;
      }
      setFile(selectedFile);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await datasetAPI.upload(file);
      // Store the data in sessionStorage to pass to dashboard
      sessionStorage.setItem('currentDataset', JSON.stringify(response.data));
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-box">
        <h1>Upload CSV File</h1>
        <p className="upload-description">
          Upload a CSV file containing chemical equipment parameters.
          Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
        </p>
        
        <form onSubmit={handleSubmit}>
          <div className="file-input-wrapper">
            <input
              type="file"
              id="file-input"
              accept=".csv"
              onChange={handleFileChange}
              disabled={loading}
            />
            <label htmlFor="file-input" className="file-input-label">
              {file ? file.name : 'Choose CSV file'}
            </label>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" disabled={loading || !file}>
            {loading ? 'Uploading...' : 'Upload and Analyze'}
          </button>
        </form>

        <div className="sample-info">
          <p>Sample CSV file available in backend/sample_equipment_data.csv</p>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;

import React from 'react';
import '../styles/DataTable.css';

const DataTable = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="no-data">No data available</div>;
  }

  return (
    <div className="data-table-container">
      <h3>Equipment Data</h3>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <tr key={index}>
                <td>{row['Equipment Name']}</td>
                <td>{row['Type']}</td>
                <td>{row['Flowrate']}</td>
                <td>{row['Pressure']}</td>
                <td>{row['Temperature']}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;

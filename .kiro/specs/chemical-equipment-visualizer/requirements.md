# Requirements Document

## Introduction

The Chemical Equipment Parameter Visualizer is a hybrid analytics platform that enables users to upload, analyze, and visualize chemical equipment parameter data through both web and desktop interfaces. The system processes CSV files containing equipment parameters (flowrate, pressure, temperature), generates statistical summaries, maintains upload history, and produces PDF reports. Both frontend applications (React web and PyQt5 desktop) connect to a unified Django REST Framework backend.

## Glossary

- **Backend System**: The Django REST Framework server that processes CSV files, manages data storage, and provides API endpoints
- **Web Client**: The React.js-based browser application using Chart.js for visualization
- **Desktop Client**: The PyQt5-based standalone application using Matplotlib for visualization
- **Dataset**: A single CSV file upload containing chemical equipment parameters
- **Summary Metrics**: Calculated statistics including counts, averages, and distributions from uploaded data
- **Upload History**: The collection of the 5 most recent dataset uploads stored in SQLite

## Requirements

### Requirement 1

**User Story:** As a chemical engineer, I want to authenticate with my credentials, so that I can securely access the system from both web and desktop interfaces

#### Acceptance Criteria

1. THE Backend System SHALL provide an authentication endpoint at /api/auth/login/ that accepts username and password
2. WHEN a user submits valid credentials, THE Backend System SHALL return an authentication token
3. THE Web Client SHALL store the authentication token and include it in subsequent API request headers
4. THE Desktop Client SHALL store the authentication token and include it in subsequent API request headers
5. WHEN a user submits invalid credentials, THE Backend System SHALL return an authentication error with HTTP status 401

### Requirement 2

**User Story:** As a user, I want to upload CSV files containing equipment parameters, so that the system can process and analyze my data

#### Acceptance Criteria

1. THE Backend System SHALL provide an upload endpoint at /api/upload/ that accepts CSV files with columns: Equipment Name, Type, Flowrate, Pressure, Temperature
2. WHEN a CSV file is uploaded, THE Backend System SHALL validate the file format and required columns
3. WHEN a valid CSV is received, THE Backend System SHALL parse the file using Pandas and store the dataset in SQLite
4. THE Backend System SHALL store the filename, upload timestamp, summary JSON, and CSV path for each upload
5. WHEN a CSV upload is processed, THE Backend System SHALL return the parsed data and calculated summary metrics to the client

### Requirement 3

**User Story:** As a user, I want the system to automatically calculate summary statistics from my uploaded data, so that I can quickly understand key metrics

#### Acceptance Criteria

1. WHEN a dataset is uploaded, THE Backend System SHALL calculate the total number of equipment rows
2. WHEN a dataset is uploaded, THE Backend System SHALL calculate the average Flowrate across all equipment
3. WHEN a dataset is uploaded, THE Backend System SHALL calculate the average Pressure across all equipment
4. WHEN a dataset is uploaded, THE Backend System SHALL calculate the average Temperature across all equipment
5. WHEN a dataset is uploaded, THE Backend System SHALL calculate the equipment type distribution showing count per type

### Requirement 4

**User Story:** As a user, I want to view my uploaded data in tables and charts, so that I can visualize patterns and distributions

#### Acceptance Criteria

1. THE Web Client SHALL display uploaded equipment data in a tabular format
2. THE Web Client SHALL render a pie chart showing equipment type distribution using Chart.js
3. THE Web Client SHALL render a bar chart showing average Flowrate, Pressure, and Temperature using Chart.js
4. THE Desktop Client SHALL display uploaded equipment data in a QTableWidget
5. THE Desktop Client SHALL render charts showing equipment type distribution and average metrics using Matplotlib

### Requirement 5

**User Story:** As a user, I want to access my upload history, so that I can review previous dataset analyses

#### Acceptance Criteria

1. THE Backend System SHALL provide a history endpoint at /api/history/ that returns the last 5 dataset uploads
2. WHEN a new dataset is uploaded, THE Backend System SHALL automatically delete the oldest upload if more than 5 uploads exist
3. THE Backend System SHALL return upload history sorted by timestamp in descending order
4. THE Web Client SHALL display the upload history with filename, timestamp, and summary metrics
5. THE Desktop Client SHALL display the upload history in a dedicated history window

### Requirement 6

**User Story:** As a user, I want to generate PDF reports of my analysis, so that I can share results with colleagues

#### Acceptance Criteria

1. THE Backend System SHALL provide a report endpoint at /api/report/pdf/ that generates PDF documents
2. THE PDF report SHALL include the application title, upload timestamp, and summary metrics
3. THE PDF report SHALL include tables showing equipment data and type distribution
4. THE Web Client SHALL provide a download mechanism for the generated PDF report
5. THE Desktop Client SHALL provide a button to download and save the generated PDF report

### Requirement 7

**User Story:** As a developer, I want the system to use a sample CSV file for testing, so that I can validate functionality during development

#### Acceptance Criteria

1. THE Backend System SHALL accept a sample CSV file named sample_equipment_data.csv for testing
2. THE sample CSV file SHALL contain representative data with all required columns
3. THE Backend System SHALL process the sample CSV file identically to user-uploaded files
4. THE Web Client SHALL successfully upload and display results from the sample CSV file
5. THE Desktop Client SHALL successfully upload and display results from the sample CSV file

### Requirement 8

**User Story:** As a system administrator, I want all API endpoints to require authentication, so that unauthorized users cannot access the system

#### Acceptance Criteria

1. THE Backend System SHALL require authentication tokens for all API endpoints except /api/auth/login/
2. WHEN a request is made without a valid authentication token, THE Backend System SHALL return HTTP status 401
3. WHEN a request is made with an expired token, THE Backend System SHALL return HTTP status 401
4. THE Web Client SHALL redirect unauthenticated users to the login page
5. THE Desktop Client SHALL display the login window when authentication is required

### Requirement 9

**User Story:** As a user, I want the web interface to have dedicated pages for different functions, so that I can navigate the application easily

#### Acceptance Criteria

1. THE Web Client SHALL provide a login page for user authentication
2. THE Web Client SHALL provide a CSV upload page with a file selection component
3. THE Web Client SHALL provide a dashboard page displaying tables, summary metrics, and charts
4. THE Web Client SHALL provide a history page listing the last 5 dataset summaries
5. THE Web Client SHALL provide navigation between all pages

### Requirement 10

**User Story:** As a user, I want the desktop application to replicate web functionality, so that I have a consistent experience across platforms

#### Acceptance Criteria

1. THE Desktop Client SHALL provide a login window for user authentication
2. THE Desktop Client SHALL provide a main dashboard with CSV upload functionality
3. THE Desktop Client SHALL display data tables and charts identical in content to the Web Client
4. THE Desktop Client SHALL provide a history window accessible from the main dashboard
5. THE Desktop Client SHALL provide PDF report download functionality identical to the Web Client

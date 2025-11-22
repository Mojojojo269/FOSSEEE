# Chemical Equipment Parameter Visualizer

A hybrid analytics platform for chemical equipment parameter analysis, available as both a web application and desktop application.

## Overview

This system allows users to:
- Upload CSV files containing chemical equipment parameters
- Receive automatically calculated summary statistics
- Visualize data using interactive charts
- Store the last 5 dataset uploads
- Generate PDF reports
- Access through authenticated login

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
├──────────────────────────┬──────────────────────────────────┤
│   React Web Client       │   PyQt5 Desktop Client           │
│   - Chart.js             │   - Matplotlib                   │
│   - Axios                │   - requests library             │
└──────────────┬───────────┴──────────────┬───────────────────┘
               │                          │
               │    HTTP/REST API         │
               │    (JSON)                │
               │                          │
┌──────────────┴──────────────────────────┴───────────────────┐
│              Django REST Framework Backend                   │
│  - Pandas (CSV processing)                                   │
│  - SQLite (data storage)                                     │
│  - ReportLab (PDF generation)                                │
└──────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Pandas 2.1.3 (CSV processing)
- SQLite (database)
- ReportLab 4.0.7 (PDF generation)
- django-cors-headers 4.3.1

### Web Frontend
- React.js 18.2.0
- Chart.js 4.4.0
- react-chartjs-2 5.2.0
- Axios 1.6.2
- React Router DOM 6.20.0
- Vite 5.0.0 (build tool)

### Desktop Frontend
- PyQt5 5.15.10
- Matplotlib 3.8.2
- Requests 2.31.0
- Pandas 2.1.3

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a test user (or create your own superuser):
```bash
python create_test_user.py
# This creates: username=testuser, password=testpass123

# Or create a superuser:
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000/api/`

### Web Frontend Setup

1. Navigate to the web directory:
```bash
cd web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The web application will be available at `http://localhost:5173/`

### Desktop Frontend Setup

1. Navigate to the desktop directory:
```bash
cd desktop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## CSV Format

The system expects CSV files with the following columns:
- **Equipment Name**: Name/ID of the equipment
- **Type**: Equipment type (e.g., Pump, Reactor, Heat Exchanger)
- **Flowrate**: Numeric value
- **Pressure**: Numeric value
- **Temperature**: Numeric value

### Sample CSV

A sample CSV file is provided at `backend/sample_equipment_data.csv`:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,150.5,45.2,85.3
Reactor-R1,Reactor,200.0,120.5,350.0
Heat Exchanger-HX1,Heat Exchanger,180.3,35.8,120.5
...
```

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### 1. Authentication

**POST** `/auth/login/`

Authenticate user and receive token.

Request:
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "testuser"
}
```

#### 2. Upload CSV

**POST** `/upload/`

Upload and process CSV file.

Headers:
```
Authorization: Token <your-token>
Content-Type: multipart/form-data
```

Request: Form data with file field

Response:
```json
{
  "dataset_id": 1,
  "filename": "sample_equipment_data.csv",
  "timestamp": "2025-11-22T18:30:00Z",
  "data": [
    {
      "Equipment Name": "Pump-A1",
      "Type": "Pump",
      "Flowrate": 150.5,
      "Pressure": 45.2,
      "Temperature": 85.3
    }
  ],
  "summary": {
    "total_count": 10,
    "avg_flowrate": 173.13,
    "avg_pressure": 62.04,
    "avg_temperature": 143.79,
    "type_distribution": {
      "Pump": 4,
      "Reactor": 2,
      "Heat Exchanger": 2,
      "Compressor": 1,
      "Mixer": 1
    }
  }
}
```

#### 3. Get History

**GET** `/history/`

Get last 5 dataset uploads.

Headers:
```
Authorization: Token <your-token>
```

Response:
```json
{
  "datasets": [
    {
      "id": 1,
      "filename": "sample_equipment_data.csv",
      "timestamp": "2025-11-22T18:30:00Z",
      "summary": { ... }
    }
  ]
}
```

#### 4. Get Summary

**GET** `/summary/<dataset_id>/`

Get summary for a specific dataset.

Headers:
```
Authorization: Token <your-token>
```

Response:
```json
{
  "id": 1,
  "filename": "sample_equipment_data.csv",
  "timestamp": "2025-11-22T18:30:00Z",
  "summary": { ... }
}
```

#### 5. Download PDF Report

**GET** `/report/pdf/<dataset_id>/`

Generate and download PDF report.

Headers:
```
Authorization: Token <your-token>
```

Response: PDF file (application/pdf)

## Features

### Authentication
- Token-based authentication
- Secure login for both web and desktop clients
- Automatic token management

### Data Processing
- CSV file validation
- Automatic statistical calculations:
  - Total equipment count
  - Average flowrate, pressure, temperature
  - Equipment type distribution
- File size limit: 10MB

### Visualization
- **Web**: Interactive Chart.js charts
  - Pie chart for equipment type distribution
  - Bar chart for average parameters
- **Desktop**: Matplotlib charts
  - Identical visualizations to web client

### History Management
- Stores last 5 dataset uploads
- Automatically removes oldest uploads
- View upload history with summaries

### PDF Reports
- Professional PDF generation
- Includes:
  - Dataset information
  - Summary statistics
  - Equipment type distribution
- Downloadable from both clients

## Dataflow

1. **User Authentication**
   - User logs in via web or desktop client
   - Backend validates credentials
   - Token returned and stored

2. **CSV Upload**
   - User selects CSV file
   - File sent to backend API
   - Backend validates and processes with Pandas
   - Summary statistics calculated
   - Data stored in SQLite
   - Results returned to client

3. **Visualization**
   - Client receives data and summary
   - Charts rendered (Chart.js or Matplotlib)
   - Data displayed in tables

4. **History & Reports**
   - User can view past uploads
   - PDF reports generated on demand
   - Files downloaded to user's system

## Project Structure

```
chemical-equipment-visualizer/
├── backend/
│   ├── api/
│   │   ├── models.py          # Dataset model
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # DRF serializers
│   │   ├── urls.py            # API routes
│   │   ├── utils.py           # CSV processing
│   │   └── permissions.py     # Auth logic
│   ├── config/
│   │   ├── settings.py        # Django settings
│   │   └── urls.py            # Root URLs
│   ├── media/uploads/         # Uploaded CSV files
│   ├── manage.py
│   ├── requirements.txt
│   └── sample_equipment_data.csv
├── web/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   ├── context/           # Auth context
│   │   └── styles/            # CSS files
│   ├── package.json
│   └── vite.config.js
├── desktop/
│   ├── windows/               # PyQt5 windows
│   ├── widgets/               # Custom widgets
│   ├── services/              # API client
│   ├── utils/                 # Config management
│   ├── main.py
│   └── requirements.txt
└── README.md
```

## Testing

### Test Credentials
- Username: `testuser`
- Password: `testpass123`

### Testing Workflow

1. Start the backend server
2. Create test user (if not already created)
3. Start web or desktop client
4. Login with test credentials
5. Upload `backend/sample_equipment_data.csv`
6. View dashboard with charts and tables
7. Check history page
8. Download PDF report

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
python manage.py runserver 8001
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

### Web Frontend Issues

**Port conflict:**
Edit `vite.config.js` to change port

**CORS errors:**
Ensure backend CORS settings include your frontend URL

### Desktop Client Issues

**PyQt5 installation fails:**
```bash
pip install PyQt5 --no-cache-dir
```

**Connection refused:**
Ensure backend is running on `http://localhost:8000`

## License

MIT License

## Contributors

Developed as part of the Chemical Equipment Parameter Visualizer project.

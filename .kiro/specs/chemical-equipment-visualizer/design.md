# Design Document

## Overview

The Chemical Equipment Parameter Visualizer is a three-tier hybrid application consisting of:

1. **Backend**: Django REST Framework API server with Pandas for data processing, SQLite for storage, and ReportLab for PDF generation
2. **Web Frontend**: React.js SPA with Chart.js for interactive visualizations
3. **Desktop Frontend**: PyQt5 application with Matplotlib for native desktop charts

Both frontends communicate with the same backend API, ensuring data consistency and centralized business logic. The system follows RESTful principles with token-based authentication.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Layer                             │
├──────────────────────────┬──────────────────────────────────┤
│   React Web Client       │   PyQt5 Desktop Client           │
│   - Chart.js             │   - Matplotlib                   │
│   - Axios/Fetch          │   - requests library             │
└──────────────┬───────────┴──────────────┬───────────────────┘
               │                          │
               │    HTTP/REST API         │
               │    (JSON)                │
               │                          │
┌──────────────┴──────────────────────────┴───────────────────┐
│              Django REST Framework Backend                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Layer (views.py)                               │   │
│  │  - Authentication                                    │   │
│  │  - File Upload Handler                              │   │
│  │  - Summary Calculator                               │   │
│  │  - History Manager                                  │   │
│  │  - PDF Generator                                    │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                          │
│  ┌────────────────┴────────────────────────────────────┐   │
│  │  Business Logic Layer                               │   │
│  │  - Pandas CSV Processing                            │   │
│  │  - Statistical Calculations                         │   │
│  │  - Data Validation                                  │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                          │
│  ┌────────────────┴────────────────────────────────────┐   │
│  │  Data Layer (models.py)                             │   │
│  │  - Dataset Model                                    │   │
│  │  - User Model (Django Auth)                         │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                          │
│  ┌────────────────┴────────────────────────────────────┐   │
│  │  SQLite Database                                    │   │
│  │  - auth_user                                        │   │
│  │  - api_dataset                                      │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Backend Components

#### 1. Django Project Structure

```
backend/
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py
├── api/
│   ├── models.py            # Dataset model
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API endpoints
│   ├── urls.py              # API routes
│   ├── utils.py             # Helper functions
│   └── permissions.py       # Authentication logic
├── media/
│   └── uploads/             # CSV file storage
├── manage.py
└── requirements.txt
```

#### 2. API Endpoints

**Authentication**
- `POST /api/auth/login/`
  - Request: `{ "username": "string", "password": "string" }`
  - Response: `{ "token": "string", "user_id": int, "username": "string" }`

**CSV Upload**
- `POST /api/upload/`
  - Headers: `Authorization: Token <token>`
  - Request: `multipart/form-data` with CSV file
  - Response: 
    ```json
    {
      "dataset_id": int,
      "filename": "string",
      "timestamp": "ISO8601",
      "data": [
        {
          "Equipment Name": "string",
          "Type": "string",
          "Flowrate": float,
          "Pressure": float,
          "Temperature": float
        }
      ],
      "summary": {
        "total_count": int,
        "avg_flowrate": float,
        "avg_pressure": float,
        "avg_temperature": float,
        "type_distribution": {
          "Pump": int,
          "Reactor": int,
          "Heat Exchanger": int
        }
      }
    }
    ```

**Summary Retrieval**
- `GET /api/summary/<dataset_id>/`
  - Headers: `Authorization: Token <token>`
  - Response: Same summary object as upload response

**Upload History**
- `GET /api/history/`
  - Headers: `Authorization: Token <token>`
  - Response:
    ```json
    {
      "datasets": [
        {
          "id": int,
          "filename": "string",
          "timestamp": "ISO8601",
          "summary": { ... }
        }
      ]
    }
    ```

**PDF Report**
- `GET /api/report/pdf/<dataset_id>/`
  - Headers: `Authorization: Token <token>`
  - Response: PDF file (application/pdf)

#### 3. Data Processing Pipeline

```python
# Pseudocode for CSV processing
def process_csv(file):
    # 1. Read CSV with Pandas
    df = pd.read_csv(file)
    
    # 2. Validate columns
    required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    validate_columns(df, required_cols)
    
    # 3. Calculate summary
    summary = {
        'total_count': len(df),
        'avg_flowrate': df['Flowrate'].mean(),
        'avg_pressure': df['Pressure'].mean(),
        'avg_temperature': df['Temperature'].mean(),
        'type_distribution': df['Type'].value_counts().to_dict()
    }
    
    # 4. Store in database
    dataset = Dataset.objects.create(
        filename=file.name,
        summary_json=json.dumps(summary),
        csv_path=save_file(file)
    )
    
    # 5. Maintain 5-record limit
    cleanup_old_datasets()
    
    return df.to_dict('records'), summary
```

### Web Frontend Components

#### 1. React Project Structure

```
web/
├── public/
├── src/
│   ├── components/
│   │   ├── Login.jsx
│   │   ├── UploadPage.jsx
│   │   ├── Dashboard.jsx
│   │   ├── HistoryPage.jsx
│   │   ├── DataTable.jsx
│   │   ├── PieChart.jsx
│   │   └── BarChart.jsx
│   ├── services/
│   │   └── api.js              # Axios API client
│   ├── context/
│   │   └── AuthContext.jsx     # Authentication state
│   ├── App.jsx
│   └── index.js
├── package.json
└── README.md
```

#### 2. Component Hierarchy

```
App
├── AuthContext.Provider
    ├── Login (route: /)
    ├── UploadPage (route: /upload)
    ├── Dashboard (route: /dashboard)
    │   ├── DataTable
    │   ├── PieChart (Chart.js)
    │   └── BarChart (Chart.js)
    └── HistoryPage (route: /history)
```

#### 3. State Management

- **Authentication**: React Context API for token and user state
- **Upload Data**: Component state in Dashboard
- **History**: Component state in HistoryPage
- **API Client**: Axios instance with interceptor for auth token

### Desktop Frontend Components

#### 1. PyQt5 Project Structure

```
desktop/
├── main.py                  # Application entry point
├── windows/
│   ├── login_window.py
│   ├── main_window.py
│   └── history_window.py
├── widgets/
│   ├── upload_widget.py
│   ├── table_widget.py
│   └── chart_widget.py
├── services/
│   └── api_client.py        # requests-based API client
├── utils/
│   └── config.py            # Token storage
└── requirements.txt
```

#### 2. Window Structure

```
LoginWindow
    ↓ (on successful login)
MainWindow
├── MenuBar
│   ├── File → Upload CSV
│   ├── View → History
│   └── Report → Download PDF
├── UploadWidget (QPushButton)
├── TableWidget (QTableWidget)
└── ChartWidget (Matplotlib canvas)
    ├── Pie Chart (equipment types)
    └── Bar Chart (averages)

HistoryWindow (QDialog)
└── HistoryListWidget (QListWidget)
```

#### 3. API Integration

```python
# Pseudocode for API client
class APIClient:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.token = None
    
    def login(self, username, password):
        response = requests.post(f"{self.base_url}/auth/login/", 
                                json={"username": username, "password": password})
        self.token = response.json()["token"]
        save_token(self.token)
    
    def upload_csv(self, filepath):
        headers = {"Authorization": f"Token {self.token}"}
        files = {"file": open(filepath, "rb")}
        response = requests.post(f"{self.base_url}/upload/", 
                                headers=headers, files=files)
        return response.json()
    
    # Similar methods for history, summary, pdf
```

## Data Models

### Backend Models

#### Dataset Model

```python
class Dataset(models.Model):
    filename = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    summary_json = models.JSONField()
    csv_path = models.FileField(upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-upload_timestamp']
```

#### User Model

Uses Django's built-in `django.contrib.auth.models.User` with token authentication via `rest_framework.authtoken`.

### Frontend Data Structures

#### Upload Response (TypeScript/Python)

```typescript
interface UploadResponse {
  dataset_id: number;
  filename: string;
  timestamp: string;
  data: EquipmentRow[];
  summary: Summary;
}

interface EquipmentRow {
  "Equipment Name": string;
  "Type": string;
  "Flowrate": number;
  "Pressure": number;
  "Temperature": number;
}

interface Summary {
  total_count: number;
  avg_flowrate: number;
  avg_pressure: number;
  avg_temperature: number;
  type_distribution: { [key: string]: number };
}
```

## Error Handling

### Backend Error Responses

All errors follow consistent JSON format:

```json
{
  "error": "string",
  "detail": "string",
  "code": "string"
}
```

**Error Codes:**
- `AUTH_FAILED`: Invalid credentials
- `INVALID_TOKEN`: Missing or expired token
- `INVALID_CSV`: CSV format or column validation failed
- `FILE_TOO_LARGE`: Uploaded file exceeds size limit
- `PROCESSING_ERROR`: Pandas processing failed
- `NOT_FOUND`: Dataset not found

### Frontend Error Handling

**Web Client:**
- Display error messages using toast notifications or alert components
- Redirect to login on 401 errors
- Show validation errors inline on upload form

**Desktop Client:**
- Display error dialogs using QMessageBox
- Return to login window on 401 errors
- Show validation errors in status bar

### Validation Rules

**CSV Validation:**
1. File must be valid CSV format
2. Required columns: Equipment Name, Type, Flowrate, Pressure, Temperature
3. Numeric columns must contain valid numbers
4. File size limit: 10MB
5. Minimum 1 row of data (excluding header)

**Authentication:**
1. Username: 3-150 characters
2. Password: minimum 8 characters
3. Token expires after 24 hours

## Testing Strategy

### Backend Testing

**Unit Tests (pytest + Django TestCase):**
- CSV parsing with valid/invalid data
- Summary calculation accuracy
- Dataset cleanup (5-record limit)
- Authentication token generation
- PDF generation

**Integration Tests:**
- Full upload workflow
- API endpoint responses
- Database transactions
- File storage

**Test Data:**
- `sample_equipment_data.csv` with 10 rows
- Edge cases: empty CSV, missing columns, invalid numbers

### Web Frontend Testing

**Unit Tests (Jest + React Testing Library):**
- Component rendering
- Form validation
- Chart data transformation
- API service functions

**Integration Tests:**
- Login flow
- Upload and display workflow
- Navigation between pages

**E2E Tests (Cypress - optional):**
- Complete user journey from login to PDF download

### Desktop Frontend Testing

**Unit Tests (pytest + pytest-qt):**
- Window initialization
- Widget interactions
- API client methods
- Chart rendering

**Integration Tests:**
- Login workflow
- CSV upload and display
- History window population

### Manual Testing Checklist

- [ ] Login with valid/invalid credentials
- [ ] Upload sample CSV and verify summary
- [ ] Verify charts display correctly
- [ ] Check history shows last 5 uploads
- [ ] Download and verify PDF content
- [ ] Test both web and desktop clients
- [ ] Verify 6th upload removes oldest

## Security Considerations

1. **Authentication**: Token-based auth with secure token storage
2. **File Upload**: Validate file type and size, sanitize filenames
3. **SQL Injection**: Use Django ORM (parameterized queries)
4. **CORS**: Configure allowed origins for web client
5. **HTTPS**: Recommend HTTPS in production
6. **Token Expiry**: Implement token refresh mechanism
7. **Input Validation**: Validate all user inputs on backend

## Deployment Considerations

**Backend:**
- Use Gunicorn/uWSGI for production
- Configure static/media file serving
- Set DEBUG=False
- Use environment variables for secrets

**Web Client:**
- Build production bundle (`npm run build`)
- Serve via Nginx or CDN
- Configure API base URL

**Desktop Client:**
- Package with PyInstaller
- Include Python runtime
- Configure default API endpoint

## Performance Optimization

1. **CSV Processing**: Stream large files instead of loading entirely in memory
2. **Database**: Index on upload_timestamp for history queries
3. **Caching**: Cache summary calculations for repeated requests
4. **Frontend**: Lazy load Chart.js and Matplotlib
5. **API**: Implement pagination for large datasets (future enhancement)

# Implementation Plan

- [x] 1. Set up project structure and initialize repositories


  - Create root directory with /backend, /web, /desktop subdirectories
  - Initialize Git repository with .gitignore for Python, Node, and IDE files
  - Create README.md with project overview and setup instructions placeholder
  - _Requirements: 7.2, 7.3_

- [x] 2. Set up Django backend project and core configuration


  - Initialize Django project in /backend directory
  - Install Django, djangorestframework, pandas, Pillow, and reportlab
  - Configure settings.py with REST framework, CORS, media files, and SQLite database
  - Create api app with models.py, views.py, serializers.py, urls.py
  - Configure root urls.py to include api routes
  - _Requirements: 1.1, 8.1_

- [x] 3. Implement authentication system


  - Install and configure rest_framework.authtoken
  - Create login API endpoint at /api/auth/login/
  - Implement token generation on successful authentication
  - Add authentication classes to REST framework settings
  - Create custom permission class requiring authentication for protected endpoints
  - _Requirements: 1.1, 1.2, 8.1, 8.2, 8.3_

- [x] 4. Create Dataset model and database schema


  - Define Dataset model with filename, upload_timestamp, summary_json, csv_path, and user foreign key
  - Add Meta class with ordering by -upload_timestamp
  - Create and run migrations
  - _Requirements: 2.4, 5.1_

- [x] 5. Implement CSV upload and processing logic


  - Create upload API endpoint at /api/upload/
  - Implement file validation (format, size, required columns)
  - Write Pandas CSV parsing function
  - Implement summary calculation function (total count, averages, type distribution)
  - Save uploaded file to media/uploads/ directory
  - Create Dataset record with summary JSON
  - Return parsed data and summary in response
  - _Requirements: 2.1, 2.2, 2.3, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 6. Implement dataset history management


  - Create cleanup function to maintain 5-record limit
  - Call cleanup function after each successful upload
  - Create history API endpoint at /api/history/
  - Implement query to return last 5 datasets with summaries
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 7. Implement PDF report generation


  - Create PDF generation function using ReportLab
  - Include title, timestamp, summary metrics, and data table in PDF
  - Create report API endpoint at /api/report/pdf/<dataset_id>/
  - Return PDF file as downloadable response
  - _Requirements: 6.1, 6.2, 6.3_

- [x] 8. Create sample CSV file for testing


  - Create sample_equipment_data.csv with 10 rows
  - Include columns: Equipment Name, Type, Flowrate, Pressure, Temperature
  - Use realistic chemical equipment data (Pump, Reactor, Heat Exchanger types)
  - Place in backend root directory
  - _Requirements: 7.1, 7.2_

- [x] 9. Write backend tests


  - [x] 9.1 Write unit tests for CSV processing and validation


    - Test valid CSV parsing
    - Test invalid CSV format handling
    - Test missing column detection
    - Test summary calculation accuracy
    - _Requirements: 2.1, 2.2, 3.1, 3.2, 3.3, 3.4, 3.5_
  - [x] 9.2 Write unit tests for authentication

    - Test login with valid credentials
    - Test login with invalid credentials
    - Test token generation
    - Test protected endpoint access with/without token
    - _Requirements: 1.1, 1.2, 1.5, 8.1, 8.2, 8.3_
  - [x] 9.3 Write integration tests for upload workflow

    - Test complete upload flow from file to database
    - Test dataset cleanup after 6th upload
    - Test history endpoint returns correct data
    - _Requirements: 2.3, 2.4, 5.1, 5.2_

- [x] 10. Set up React web client project


  - Initialize React app in /web directory using create-react-app or Vite
  - Install dependencies: react-router-dom, axios, chart.js, react-chartjs-2
  - Configure proxy or API base URL for backend communication
  - Set up project structure with components/, services/, context/ directories
  - _Requirements: 9.1_

- [x] 11. Implement web authentication and routing


  - Create AuthContext for managing token and user state
  - Implement Login component with form and validation
  - Create API service with axios instance and auth interceptor
  - Implement login API call and token storage in localStorage
  - Set up React Router with protected routes
  - Create navigation component
  - _Requirements: 1.3, 8.4, 9.1, 9.5_

- [x] 12. Implement web CSV upload page


  - Create UploadPage component with file input
  - Implement file selection and upload handler
  - Call /api/upload/ endpoint with multipart form data
  - Display upload progress or loading state
  - Navigate to dashboard on successful upload
  - Display error messages on upload failure
  - _Requirements: 2.1, 9.2_

- [x] 13. Implement web dashboard with data display


  - Create Dashboard component to receive upload response
  - Create DataTable component to display equipment data in HTML table
  - Display summary metrics (total count, averages) in cards or panels
  - Store uploaded data and summary in component state
  - _Requirements: 4.1, 9.3_

- [x] 14. Implement web charts using Chart.js


  - Create PieChart component for equipment type distribution
  - Create BarChart component for average Flowrate, Pressure, Temperature
  - Transform summary data into Chart.js format
  - Integrate charts into Dashboard component
  - Configure chart options for readability
  - _Requirements: 4.2, 4.3_

- [x] 15. Implement web history page


  - Create HistoryPage component
  - Call /api/history/ endpoint on component mount
  - Display list of last 5 uploads with filename, timestamp, and summary
  - Add navigation link from dashboard to history page
  - _Requirements: 5.4, 9.4_

- [x] 16. Implement web PDF download functionality

  - Add download PDF button to Dashboard component
  - Call /api/report/pdf/<dataset_id>/ endpoint
  - Handle blob response and trigger browser download
  - Display success/error messages
  - _Requirements: 6.4_

- [x] 17. Write web frontend tests


  - [x] 17.1 Write component unit tests


    - Test Login component rendering and form submission
    - Test DataTable component with mock data
    - Test chart components with mock summary data
    - _Requirements: 9.1, 9.2, 9.3_
  - [x] 17.2 Write integration tests for user flows


    - Test login flow with AuthContext
    - Test upload and dashboard display flow
    - Test navigation between pages
    - _Requirements: 1.3, 2.1, 9.5_

- [x] 18. Set up PyQt5 desktop client project


  - Create /desktop directory with main.py entry point
  - Install dependencies: PyQt5, matplotlib, requests, pandas
  - Create project structure with windows/, widgets/, services/ directories
  - Set up basic application initialization
  - _Requirements: 1.4_

- [x] 19. Implement desktop API client service


  - Create APIClient class using requests library
  - Implement login method with token storage
  - Implement upload_csv method with multipart file upload
  - Implement get_history and get_pdf methods
  - Store token in config file or system keyring
  - _Requirements: 1.4, 8.5_

- [x] 20. Implement desktop login window


  - Create LoginWindow class inheriting QDialog
  - Add username and password QLineEdit widgets
  - Add login QPushButton
  - Implement login handler calling APIClient.login()
  - Display error QMessageBox on authentication failure
  - Open MainWindow on successful login
  - _Requirements: 1.4, 8.5_

- [x] 21. Implement desktop main window structure


  - Create MainWindow class inheriting QMainWindow
  - Add menu bar with File, View, Report menus
  - Create central widget with vertical layout
  - Add upload button at top
  - Add QTableWidget for data display
  - Add matplotlib canvas widget for charts
  - _Requirements: 10.2, 10.3_

- [x] 22. Implement desktop CSV upload functionality

  - Add "Upload CSV" action to File menu
  - Implement file dialog for CSV selection
  - Call APIClient.upload_csv() with selected file
  - Parse response and update table widget with data
  - Display summary metrics in status bar or label
  - Handle upload errors with QMessageBox
  - _Requirements: 2.1, 10.2_

- [x] 23. Implement desktop data table display

  - Configure QTableWidget with appropriate columns
  - Populate table with equipment data from upload response
  - Set column headers: Equipment Name, Type, Flowrate, Pressure, Temperature
  - Enable sorting and resizing
  - _Requirements: 4.4, 10.3_

- [x] 24. Implement desktop charts using Matplotlib


  - Create chart widget with matplotlib FigureCanvas
  - Implement pie chart for equipment type distribution
  - Implement bar chart for average metrics
  - Update charts when new data is uploaded
  - Match chart styling to web version
  - _Requirements: 4.5, 10.3_

- [x] 25. Implement desktop history window


  - Create HistoryWindow class inheriting QDialog
  - Add QListWidget to display upload history
  - Call APIClient.get_history() on window open
  - Display filename, timestamp, and summary for each dataset
  - Add "View History" action to View menu
  - _Requirements: 5.5, 10.4_

- [x] 26. Implement desktop PDF download functionality

  - Add "Download PDF" action to Report menu
  - Call APIClient.get_pdf() with current dataset_id
  - Open file save dialog for PDF destination
  - Write PDF bytes to selected file
  - Display success message on completion
  - _Requirements: 6.5, 10.5_

- [x] 27. Write desktop frontend tests


  - [x] 27.1 Write unit tests for API client


    - Test login method with mock responses
    - Test upload_csv method with mock file
    - Test error handling for network failures
    - _Requirements: 1.4, 2.1_
  - [x] 27.2 Write widget tests using pytest-qt


    - Test LoginWindow initialization and login flow
    - Test MainWindow upload button functionality
    - Test table widget population
    - _Requirements: 10.2, 10.3_

- [x] 28. Create comprehensive documentation



  - Write detailed setup instructions in README.md for all three components
  - Document API endpoints with request/response examples
  - Create architecture diagram showing system components
  - Document dataflow from CSV upload to visualization
  - Add screenshots of web and desktop interfaces
  - Document sample CSV format and requirements
  - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 29. Perform end-to-end integration testing



  - Start Django backend server
  - Test web client complete workflow: login → upload → dashboard → history → PDF
  - Test desktop client complete workflow: login → upload → charts → history → PDF
  - Verify both clients show consistent data from same backend
  - Test with sample_equipment_data.csv
  - Verify 5-record history limit works correctly
  - _Requirements: 7.1, 7.2, 7.3, 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 30. Finalize project deliverables



  - Review and update all documentation
  - Ensure .gitignore excludes sensitive files and dependencies
  - Create requirements.txt for backend and desktop
  - Create package.json for web client
  - Add license file if applicable
  - Verify all code follows consistent style
  - Push final version to GitHub repository
  - _Requirements: 7.1, 7.2_

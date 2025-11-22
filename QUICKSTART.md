# Quick Start Guide

Get the Chemical Equipment Parameter Visualizer up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

## 1. Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create test user
python create_test_user.py

# Start server
python manage.py runserver
```

Backend will be running at `http://localhost:8000`

## 2. Web Client Setup (1 minute)

Open a new terminal:

```bash
# Navigate to web
cd web

# Install dependencies
npm install

# Start development server
npm run dev
```

Web app will be running at `http://localhost:5173`

## 3. Desktop Client Setup (1 minute)

Open a new terminal:

```bash
# Navigate to desktop
cd desktop

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## 4. Test the System (1 minute)

### Web Client
1. Open browser to `http://localhost:5173`
2. Login with: `testuser` / `testpass123`
3. Upload `backend/sample_equipment_data.csv`
4. View dashboard with charts
5. Check history page
6. Download PDF report

### Desktop Client
1. Launch application
2. Login with: `testuser` / `testpass123`
3. Click "Choose File and Upload"
4. Select `backend/sample_equipment_data.csv`
5. View data table and charts
6. Open View → History
7. Download PDF via Report → Download PDF

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Ensure virtual environment is activated
- Run `python manage.py migrate` again

### Web client won't start
- Check if port 5173 is available
- Delete `node_modules` and run `npm install` again
- Clear browser cache

### Desktop client won't start
- Ensure PyQt5 is installed correctly
- Check if backend is running
- Verify Python version is 3.8+

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [API Documentation](README.md#api-documentation) for endpoint details
- Review [INTEGRATION_TEST.md](INTEGRATION_TEST.md) for test scenarios
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Support

For issues or questions, please open an issue on GitHub.

---

**Congratulations!** You now have a fully functional Chemical Equipment Parameter Visualizer system running locally.

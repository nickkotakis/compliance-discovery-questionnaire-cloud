# Compliance Discovery Questionnaire - Startup Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Quick Start (Recommended)

### Option 1: Automated Startup

Run the health check first to verify everything is configured:
```bash
cd compliance-questionnaire
./health-check.sh
```

If all checks pass, start the application:
```bash
./start.sh
```

This will:
1. Set up a Python virtual environment
2. Install all backend dependencies
3. Start the backend API server on http://localhost:5000
4. Install frontend dependencies
5. Start the frontend dev server on http://localhost:5174

### Option 2: Manual Startup

#### Backend

1. Navigate to backend directory:
```bash
cd compliance-questionnaire/backend
```

2. Create and activate virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

4. Start the API server:
```bash
python compliance_discovery/api_server.py
```

The backend will be available at http://localhost:5000

#### Frontend

1. Open a new terminal and navigate to frontend directory:
```bash
cd compliance-questionnaire/frontend
```

2. Install dependencies (first time only):
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:5174

## Verifying the Installation

1. Check backend health:
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-..."
}
```

2. Open your browser and navigate to http://localhost:5174

3. You should see the Compliance Discovery Questionnaire interface

## Common Issues

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'compliance_discovery'`
**Solution**: Make sure you installed the package with `pip install -e .` from the backend directory

**Issue**: `ImportError: No module named 'flask'`
**Solution**: Install dependencies with `pip install -r requirements.txt`

**Issue**: Port 5000 already in use
**Solution**: Either stop the process using port 5000 or modify the port in `api_server.py`

### Frontend Issues

**Issue**: `Cannot find module 'react'`
**Solution**: Run `npm install` in the frontend directory

**Issue**: Port 5174 already in use
**Solution**: Vite will automatically try the next available port (5175, 5176, etc.)

**Issue**: API connection errors
**Solution**: Make sure the backend server is running on http://localhost:5000

## Testing

### Backend Tests
```bash
cd compliance-questionnaire/backend
pytest
```

### Frontend Build Test
```bash
cd compliance-questionnaire/frontend
npm run build
```

## Stopping the Application

- If using `start.sh`: Press `Ctrl+C` in the terminal
- If running manually: Press `Ctrl+C` in each terminal window

## Next Steps

1. Read the [README.md](README.md) for detailed documentation
2. Check the [QUICKSTART_COMPLIANCE.md](QUICKSTART_COMPLIANCE.md) for usage examples
3. Review the API documentation in the backend README

## Support

For issues or questions, refer to:
- Backend README: `backend/README.md`
- Frontend README: `frontend/README.md`
- Main README: `README.md`

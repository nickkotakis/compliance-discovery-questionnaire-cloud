# Quick Start Guide - Compliance Discovery Questionnaire

Get up and running with the Compliance Discovery Questionnaire in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

## Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Start the API server
python compliance_discovery/api_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Keep this terminal open!

## Step 2: Frontend Setup (2 minutes)

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

You should see:
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:5174/
```

## Step 3: Use the Application (1 minute)

1. Open your browser to `http://localhost:5174`
2. Click "New Session" button
3. Enter customer and analyst names
4. Click "Create Session"
5. Start answering compliance questions!

## Common Tasks

### Export a Template
1. Click "Export Template" button in the header
2. Choose your format (JSON, Excel, PDF, YAML)
3. Template downloads automatically

### Complete an Assessment
1. Create a new session
2. Answer all questions in the questionnaire
3. Provide evidence and notes as needed
4. Export the completed assessment

### Run Tests
```bash
cd backend
pytest
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.8+)
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check if port 5000 is available

### Frontend won't start
- Check Node version: `node --version` (should be 18+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 5174 is available

### API connection errors
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Verify API URL in `frontend/src/services/complianceApi.ts`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API documentation](COMPLIANCE_INTEGRATION_README.md)
- Review [implementation details](COMPLIANCE_IMPLEMENTATION_SUMMARY.md)
- Check out example usage in `backend/example_usage.py`

## Example Usage (Python)

```python
from compliance_discovery import ComplianceQuestionnaire

# Create questionnaire
q = ComplianceQuestionnaire(
    frameworks=['NIST 800-53', 'AWS'],
    customer_name='Acme Corp',
    analyst_name='Jane Smith'
)

# Generate questions
questions = q.generate_questions()

# Export to Excel
q.export_to_excel('assessment.xlsx')
```

## Support

For detailed documentation, see the `.kiro/specs/compliance-discovery-questionnaire/` directory.

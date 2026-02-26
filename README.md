# Compliance Discovery Questionnaire

An intelligent compliance assessment tool that generates dynamic questionnaires based on NIST 800-53 and AWS security frameworks. This tool helps security analysts conduct comprehensive compliance assessments with automated question generation, evidence tracking, and multi-format export capabilities.

## Features

### Backend (Python)
- **Dynamic Question Generation**: Automatically generates relevant compliance questions based on NIST 800-53 controls and AWS security best practices
- **Multi-Framework Support**: Integrates NIST 800-53 and AWS security frameworks
- **Evidence Tracking**: Comprehensive evidence collection and documentation
- **Multi-Format Export**: Export questionnaires in JSON, YAML, Excel, and PDF formats
- **RESTful API**: Flask-based API server for frontend integration
- **Session Management**: Track multiple assessment sessions with customer and analyst information

### Frontend (React + TypeScript)
- **Interactive Questionnaire Interface**: Clean, user-friendly interface for conducting assessments
- **Real-time Progress Tracking**: Visual progress indicators for assessment completion
- **Session Management**: Create and manage multiple assessment sessions
- **Template Export**: Download questionnaire templates in various formats
- **Responsive Design**: Works seamlessly on desktop and tablet devices

## Quick Start

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Run the API server:
```bash
python compliance_discovery/api_server.py
```

The API server will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:5174`

## Architecture

### Backend Structure
```
backend/
├── compliance_discovery/       # Main package
│   ├── __init__.py
│   ├── api_server.py          # Flask API server
│   ├── nist_parser.py         # NIST 800-53 parser
│   ├── question_generator.py  # Question generation logic
│   ├── export_generator.py    # Multi-format export
│   ├── excel_helpers.py       # Excel formatting utilities
│   ├── exceptions.py          # Custom exceptions
│   └── models/                # Data models
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
└── pytest.ini                 # Test configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   └── ComplianceQuestionnaire.tsx  # Main questionnaire component
│   ├── services/
│   │   └── complianceApi.ts             # API client
│   ├── pages/
│   │   └── Compliance.tsx               # Main page
│   ├── App.tsx                          # App entry point
│   ├── main.tsx                         # React entry point
│   └── index.css                        # Global styles
├── public/                    # Static assets
├── package.json              # Node dependencies
├── vite.config.ts            # Vite configuration
└── tsconfig.json             # TypeScript configuration
```

## API Endpoints

### Session Management
- `POST /api/sessions` - Create a new assessment session
- `GET /api/sessions/<session_id>` - Get session details

### Question Management
- `GET /api/questions` - Get all questions for a session
- `POST /api/questions/<question_id>/answer` - Submit an answer

### Export
- `GET /api/export/template` - Export questionnaire template
- `GET /api/export/session/<session_id>` - Export completed assessment

## Usage Examples

### Creating a Session
```python
from compliance_discovery import ComplianceQuestionnaire

# Initialize questionnaire
questionnaire = ComplianceQuestionnaire(
    frameworks=['NIST 800-53', 'AWS'],
    customer_name='Acme Corp',
    analyst_name='John Doe'
)

# Generate questions
questions = questionnaire.generate_questions()
```

### Exporting Results
```python
# Export to Excel
questionnaire.export_to_excel('assessment.xlsx')

# Export to PDF
questionnaire.export_to_pdf('assessment.pdf')

# Export to JSON
questionnaire.export_to_json('assessment.json')
```

## Documentation

- [Quick Start Guide](QUICKSTART_COMPLIANCE.md) - Get started quickly
- [Implementation Summary](COMPLIANCE_IMPLEMENTATION_SUMMARY.md) - Technical details
- [Integration Guide](COMPLIANCE_INTEGRATION_README.md) - Integration instructions
- [Specifications](.kiro/specs/compliance-discovery-questionnaire/) - Detailed specifications

## Technology Stack

### Backend
- Python 3.8+
- Flask (API server)
- openpyxl (Excel generation)
- reportlab (PDF generation)
- PyYAML (YAML support)
- pytest (testing)

### Frontend
- React 18
- TypeScript
- Vite (build tool)
- Lucide React (icons)

## Testing

Run backend tests:
```bash
cd backend
pytest
```

## Development

### Backend Development
```bash
cd backend
pip install -e .
python compliance_discovery/api_server.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

## License

Proprietary - Internal Use Only

## Support

For questions or issues, please refer to the documentation in the `.kiro/specs/` directory or contact the development team.

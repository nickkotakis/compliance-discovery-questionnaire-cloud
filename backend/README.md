# Compliance Discovery Backend

Python backend for the Compliance Discovery Questionnaire application.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Run the API server:
```bash
python compliance_discovery/api_server.py
```

The API will be available at `http://localhost:5000`

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=compliance_discovery
```

## Example Usage

See `example_usage.py` and `example_compliance_usage.py` for usage examples.

## API Endpoints

- `POST /api/sessions` - Create assessment session
- `GET /api/sessions/<id>` - Get session details
- `GET /api/questions` - Get questions
- `POST /api/questions/<id>/answer` - Submit answer
- `GET /api/export/template` - Export template
- `GET /api/export/session/<id>` - Export session

## Project Structure

```
compliance_discovery/
├── __init__.py
├── api_server.py          # Flask API server
├── nist_parser.py         # NIST 800-53 parser
├── question_generator.py  # Question generation
├── export_generator.py    # Multi-format export
├── excel_helpers.py       # Excel utilities
├── exceptions.py          # Custom exceptions
└── models/                # Data models
```

## Dependencies

- Flask - API server
- openpyxl - Excel generation
- reportlab - PDF generation
- PyYAML - YAML support
- pytest - Testing framework

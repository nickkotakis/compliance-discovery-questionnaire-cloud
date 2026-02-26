# Compliance Discovery Questionnaire Integration

This document describes the complete integration of the Compliance Discovery Questionnaire tool with the SaaS Risk Dashboard.

## Overview

The integration provides a comprehensive compliance assessment system based on NIST 800-53 Rev 5 Moderate Baseline, with support for:

- **325+ NIST 800-53 controls** from the Moderate Baseline
- **Discovery questions** for each control (8-10 questions per control)
- **AWS control mappings** via compass-control-guides MCP server
- **Multi-framework support** (NIST CSF, GLBA, SOX, FFIEC, AWS)
- **Session management** for tracking assessment progress
- **Template export** for offline completion

## Architecture

### Backend Components

1. **NIST Parser** (`compliance_discovery/nist_parser.py`)
   - Retrieves OSCAL profile and catalog from NIST GitHub
   - Parses Moderate Baseline controls
   - Extracts control details, parameters, and enhancements

2. **Question Generator** (`compliance_discovery/question_generator.py`)
   - Generates 8-10 discovery questions per control
   - Covers: current state, implementation, maturity, evidence, parameters, second/third line defense, audit readiness, continuous monitoring
   - Includes AWS service guidance for audit readiness questions

3. **MCP Integration** (`compliance_discovery/mcp_integration.py`)
   - Integrates with compass-control-guides MCP server
   - Maps NIST controls to AWS Config rules, Security Hub controls, Control Tower IDs
   - Provides AWS implementation hints

4. **API Server** (`compliance_discovery/api_server.py`)
   - Flask REST API with CORS support
   - Endpoints for controls, questions, sessions, and template export
   - In-memory caching for performance

### Frontend Components

1. **API Client** (`src/services/complianceApi.ts`)
   - TypeScript client for backend API
   - Type-safe interfaces for all data models
   - Error handling and request management

2. **Questionnaire Component** (`src/components/ComplianceQuestionnaire.tsx`)
   - Interactive control browser with family filtering
   - Expandable control details with questions
   - AWS hints display
   - Response capture and auto-save

3. **Compliance Page** (`src/pages/Compliance.tsx`)
   - Session management UI
   - Template export functionality
   - Navigation and header

## Installation

### Backend Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- Flask >= 3.0.0
- flask-cors >= 4.0.0
- requests >= 2.31.0
- openpyxl >= 3.1.2
- reportlab >= 4.0.7
- PyYAML >= 6.0.1

### Frontend Dependencies

No additional dependencies required. The project already includes:
- React
- React Router
- TypeScript
- Lucide React (icons)

## Usage

### Starting the Backend API

```bash
python compliance_discovery/api_server.py
```

The API server will:
1. Start on `http://localhost:5000`
2. Load NIST 800-53 Moderate Baseline controls (~325 controls)
3. Generate discovery questions (~2,600 questions)
4. Be ready to serve requests

**Note:** Initial startup takes 10-30 seconds to download and parse OSCAL data from NIST GitHub.

### Starting the Frontend

```bash
npm run dev
```

Then navigate to `http://localhost:5173/compliance`

### Using the Application

1. **Browse Controls**
   - View all Moderate Baseline controls
   - Filter by control family (AC, AU, CM, etc.)
   - Click to expand control details

2. **Answer Questions**
   - Each control has 8-10 discovery questions
   - Questions cover implementation, maturity, evidence, etc.
   - Responses auto-save when you leave the field

3. **View AWS Hints**
   - AWS implementation hints shown for each control
   - Includes Config rules, Security Hub controls, Control Tower IDs
   - AWS service guidance for audit readiness

4. **Create Sessions**
   - Click "New Session" to start an assessment
   - Enter customer and analyst names
   - Session tracks all responses

5. **Export Template**
   - Click "Export Template" to download blank questionnaire
   - JSON format with all controls and questions
   - Can be completed offline and imported later

## API Endpoints

### Health Check
```
GET /api/health
```

### Get All Controls
```
GET /api/controls?family=AC
```

### Get Control Details
```
GET /api/controls/AC-1
```
Returns control with questions and AWS hints.

### Get Questions
```
GET /api/questions?control_id=AC-1&question_type=implementation
```

### Create Session
```
POST /api/session
Body: {
  "customer_name": "Example Bank",
  "analyst_name": "John Doe",
  "frameworks": ["NIST 800-53", "AWS"]
}
```

### Record Response
```
POST /api/session/{session_id}/response
Body: {
  "question_id": "AC-1-IMPLEMENTATION",
  "answer": "We implement this control using...",
  "notes": "Additional notes"
}
```

### Export Template
```
GET /api/export?format=json
```

## Data Models

### Control
```typescript
interface Control {
  id: string;              // e.g., "AC-1"
  title: string;
  description: string;
  family: string;          // e.g., "AC"
  in_moderate_baseline: boolean;
  parameters?: Parameter[];
  enhancements?: Enhancement[];
}
```

### Question
```typescript
interface Question {
  id: string;
  control_id: string;
  question_text: string;
  question_type: string;   // current_state, implementation, maturity, etc.
  family: string;
  aws_service_guidance?: string;
}
```

### Session
```typescript
interface Session {
  id: string;
  customer_name: string;
  analyst_name: string;
  frameworks: string[];
  created_at: string;
  updated_at: string;
  status: string;
  responses: Record<string, Response>;
  evidence: Record<string, any>;
}
```

## Question Types

Each control has questions covering:

1. **CURRENT_STATE** - Current implementation status
2. **IMPLEMENTATION** - Specific processes and technologies
3. **MATURITY** - Maturity level assessment
4. **EVIDENCE** - Evidence availability and location
5. **PARAMETER** - Parameter value selection (if applicable)
6. **SECOND_LINE_DEFENSE** - Compliance and risk oversight
7. **THIRD_LINE_DEFENSE** - Internal audit readiness
8. **AUDIT_READINESS** - Automated reporting and evidence
9. **CONTINUOUS_MONITORING** - Monitoring and alerting

## AWS Service Guidance

For audit readiness and continuous monitoring questions, the system provides guidance on relevant AWS services:

- **CloudWatch** - Metrics, logs, and alarms
- **Security Hub** - Centralized security findings
- **AWS Config** - Configuration compliance tracking
- **Systems Manager** - Operational data collection
- **AWS Audit Manager** - Continuous audit readiness

Family-specific guidance is also provided (e.g., IAM Access Analyzer for AC family, CloudTrail for AU family).

## MCP Integration

The system integrates with the compass-control-guides MCP server to provide:

- **707+ AWS Control Guides** with framework mappings
- **480+ AWS Config rules**
- **322+ Security Hub controls**
- **465+ Control Tower controls**
- **Bidirectional mappings** between NIST 800-53 and AWS controls

**Note:** MCP integration is currently a placeholder. To enable full MCP functionality, implement the actual MCP protocol in `compliance_discovery/mcp_integration.py`.

## Troubleshooting

### API Server Won't Start

**Problem:** `ModuleNotFoundError` or import errors

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Controls Not Loading

**Problem:** "Failed to load controls" error in UI

**Solution:** 
1. Ensure API server is running on port 5000
2. Check console for CORS errors
3. Verify network connectivity to NIST GitHub

### Slow Initial Load

**Problem:** API takes 30+ seconds to start

**Solution:** This is normal. The system downloads and parses ~325 controls from NIST GitHub on first load. Subsequent requests are fast due to caching.

### AWS Hints Not Showing

**Problem:** No AWS hints displayed for controls

**Solution:** 
1. MCP integration is currently a placeholder
2. Implement actual MCP protocol in `mcp_integration.py`
3. Or use static AWS mapping data

## Future Enhancements

1. **Database Integration** - Replace in-memory storage with PostgreSQL/MongoDB
2. **MCP Protocol Implementation** - Complete MCP server integration
3. **Multi-format Export** - Add Excel, PDF, CSV export formats
4. **Evidence Management** - Add evidence upload and tracking
5. **Framework Mapper** - Add NIST CSF, GLBA, SOX, FFIEC mappings
6. **Session Persistence** - Save sessions to disk/database
7. **Progress Tracking** - Visual progress indicators and coverage analysis
8. **Collaboration** - Multi-user sessions with real-time updates

## Testing

Run tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=compliance_discovery tests/
```

## License

This integration follows the same license as the parent project.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the design document in `.kiro/specs/compliance-discovery-questionnaire/design.md`
3. Check API server logs for detailed error messages

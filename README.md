# Compliance Discovery Questionnaire

An interactive compliance assessment tool that generates framework-specific discovery questionnaires for AWS environments. Built for AWS Security Assurance Services (SAS) advisors to guide structured compliance conversations with customers.

> **Internal Use Only**: This tool is intended for AWS SAS authorized personnel and designated team members.

> **Advisory Services Only**: AWS SAS provides technical consulting exclusively and does not provide legal advice, formal audits, or compliance certifications. Legal counsel is required for regulatory interpretation.

## Supported Frameworks

- **NIST 800-53 Rev 5 (Moderate Baseline)** — 134 controls across 20 families
- **NIST CSF 2.0** — 103 subcategories across 6 functions (Govern, Identify, Protect, Detect, Respond, Recover)

## Features

- Framework-specific questionnaires with multi-layered question types (Implementation, Evidence, Second Line Defense, Third Line Defense, Audit Readiness)
- AWS control mappings showing relevant Config rules, Security Hub controls, and Control Tower guardrails per control
- AWS Implementation Guide panel with service-specific guidance
- Ownership badges (AWS / Customer / Shared) on each control
- Custom implementation questions for all 103 CSF subcategories and 134 NIST 800-53 controls
- Targeted evidence questions requesting specific auditable artifacts (IAM credential reports, Config compliance reports, KMS key policies, etc.)
- Family-level evidence templates for NIST 800-53 with keyword-matched specialization
- Session management with DynamoDB persistence
- PDF and Excel export
- Cloudscape Design System UI

## Architecture

```
frontend/          React + TypeScript + Cloudscape Design System
  src/
    components/    ComplianceQuestionnaire.tsx (main UI)
    services/      complianceApi.ts (API client)

backend/
  compliance_discovery/
    api_server.py              Flask API (served via Mangum on Lambda)
    control_questions.py       NIST 800-53 custom implementation + evidence questions
    csf_custom_questions.py    NIST CSF 2.0 custom implementation + evidence questions
    evidence_questions.py      NIST 800-53 family-level evidence templates
    question_generator.py      Question generation engine
    csf_parser.py              CSF 2.0 data parser
    csf_data.json              CSF 2.0 subcategory definitions
    csf_aws_mappings.json      CSF-to-AWS control mappings
    aws_controls_data.json     800-53-to-AWS control mappings
    aws_controls_mcp_data.json Extended AWS control data
    models/                    Data models (Control, Question, Session)

cdk/               AWS CDK infrastructure
  cdk/
    compliance_discovery_stack.py   Lambda + API Gateway + S3 + CloudFront + DynamoDB
```

## Prerequisites

- Node.js 20+
- Python 3.11+
- AWS CLI configured with appropriate credentials
- AWS CDK CLI (`npm install -g aws-cdk`)

## Local Development

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m compliance_discovery.api_server
```

The API runs on `http://localhost:5000` by default.

## Deployment

### Infrastructure (CDK)

The stack deploys:
- Lambda function (Python 3.11) with the backend API
- API Gateway (REST) with proxy integration
- S3 bucket for frontend static hosting
- CloudFront distribution
- DynamoDB table for session persistence

```bash
cd cdk
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
npx cdk deploy --profile <your-aws-profile>
```

### Frontend Deployment (after CDK is set up)

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://<frontend-bucket-name> --delete --profile <your-aws-profile>
aws cloudfront create-invalidation --distribution-id <distribution-id> --paths "/*" --profile <your-aws-profile>
```

## Question Generation

The questionnaire generates 5 question types per control:

| Type | Purpose |
|------|---------|
| Implementation | How is the control implemented in AWS? Specific services, configurations, processes |
| Evidence | What auditable artifacts demonstrate compliance? Specific documents, reports, logs |
| Second Line Defense / Maturity | How does the compliance team verify the control? Oversight mechanisms |
| Third Line Defense | Is the implementation audit-ready? Documentation gaps |
| Audit Readiness / Gaps | Can evidence be quickly produced for auditors? Improvement opportunities |

### Evidence Question Hierarchy

For NIST 800-53:
1. Specific custom evidence questions (91 controls with tailored artifact requests)
2. Family-level evidence templates with keyword matching (covers remaining controls across all 20 families)
3. Generic fallback (policy controls get policy-specific questions, technical controls get AWS service-specific questions)

For NIST CSF 2.0:
1. Custom evidence questions for all 103 subcategories requesting specific artifacts
2. AWS service-based fallback for any unmapped subcategories

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/frameworks` | List available frameworks |
| GET | `/api/controls?framework=<id>` | List all controls for a framework |
| GET | `/api/controls/<control_id>?framework=<id>` | Get control detail with questions and AWS mappings |
| GET | `/api/questions?framework=<id>` | Get all questions |
| POST | `/api/session` | Create assessment session |
| GET | `/api/session/<id>` | Get session details |
| POST | `/api/session/<id>/response` | Record a question response |
| GET | `/api/sessions` | List all sessions |
| GET | `/api/export?session_id=<id>&format=<pdf\|excel>` | Export assessment |

## Key Files

| File | Description |
|------|-------------|
| `control_questions.py` | 134 NIST 800-53 controls with custom implementation and evidence questions |
| `csf_custom_questions.py` | 103 CSF subcategories with custom implementation questions + 103 evidence questions |
| `evidence_questions.py` | 20 family-level evidence templates for 800-53 (policy, technical, keyword variants) |
| `question_generator.py` | Core engine that assembles questions from all sources |
| `csf_aws_mappings.json` | 718 AWS control entries mapped to 105 CSF subcategories |
| `aws_controls_data.json` | AWS Config rules, Security Hub controls, and services mapped to 800-53 controls |

## Disclaimer

This tool is provided by AWS Security Assurance Services (AWS SAS) for internal advisory use. AWS SAS provides technical consulting services exclusively and does not provide legal advice, formal audits, compliance certifications, or regulatory approval. All outputs are designed to support — not replace — professional judgment and independent validation. Legal counsel is required for regulatory interpretation.

© 2026 Amazon Web Services, Inc. or its affiliates. All rights reserved.

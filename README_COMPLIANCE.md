# Compliance Discovery Questionnaire Tool

A Python-based system for facilitating structured compliance assessment sessions for banking institutions using NIST 800-53 Revision 5 Moderate Baseline.

## Overview

This tool helps compliance analysts conduct systematic assessments of banking institutions' compliance posture across multiple regulatory frameworks:

- **NIST 800-53 Rev 5 Moderate Baseline**: Primary control set (~325 controls)
- **NIST Cybersecurity Framework (CSF)**: Functions and categories
- **GLBA**: Gramm-Leach-Bliley Act requirements
- **SOX**: Sarbanes-Oxley Act sections 302 and 404
- **FFIEC**: Federal Financial Institutions Examination Council standards
- **AWS Controls**: AWS Config rules, Security Hub controls, Control Tower controls

## Key Features

### 1. Blank Questionnaire Template Export

Export pre-populated templates with all Moderate Baseline controls, discovery questions, framework mappings, and AWS hints for offline completion:

- **Excel**: Multi-sheet workbook with formatted sections
- **CSV**: Separate files for controls, questions, mappings, evidence
- **PDF**: Formatted document with table of contents
- **JSON**: Structured data for programmatic processing
- **YAML**: Human-readable structured format

### 2. Multi-Framework Mapping

Automatically map NIST 800-53 controls to other frameworks:
- Complete one NIST assessment
- Get compliance status across all mapped frameworks
- Identify gaps and coverage percentages

### 3. AWS Control Integration

Integration with compass-control-guides MCP server provides:
- 707+ AWS Control Guides
- AWS Config rule mappings
- Security Hub control mappings
- Control Tower control mappings

### 4. Evidence Documentation

Capture evidence for each control:
- Evidence description (what it is)
- Evidence location (where it's stored)
- Additional notes and observations

### 5. Discovery Question Types

Comprehensive question types guide assessment:
- **Current State**: Describe existing implementation
- **Implementation**: Assess how controls are implemented
- **Maturity**: Evaluate sophistication and effectiveness
- **Evidence**: Identify available documentation
- **Gap Analysis**: Identify deficiencies
- **Remediation**: Explore compliance steps
- **AWS Implementation**: Consider AWS services
- **Second Line Defense**: Assess compliance review readiness
- **Third Line Defense**: Assess internal audit readiness
- **Audit Readiness**: Evaluate automated reporting
- **Continuous Monitoring**: Assess automated monitoring

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd compliance-discovery-questionnaire

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### Export a Blank Template

```python
from compliance_discovery.export_generator import ExportGenerator
from compliance_discovery.models import Control, DiscoveryQuestion, FrameworkMappings

# Initialize generator
generator = ExportGenerator()

# Load your controls, questions, and mappings
# (In production, these would come from NIST parser and framework mapper)
controls = [...]  # List of Control objects
questions = {...}  # Dict mapping control_id to list of DiscoveryQuestion objects
mappings = {...}   # Dict mapping control_id to FrameworkMappings objects

generator.set_controls(controls)
generator.set_questions(questions)
generator.set_framework_mappings(mappings)
generator.set_mcp_available(True)  # If MCP server is available

# Prepare template
template = generator.prepare_blank_template()

# Export to Excel
excel_bytes = generator.export_blank_template_excel(template)
with open("questionnaire.xlsx", "wb") as f:
    f.write(excel_bytes)

# Export to CSV
csv_files = generator.export_blank_template_csv(template)
for filename, content in csv_files.items():
    with open(filename, "w") as f:
        f.write(content)

# Export to PDF
pdf_bytes = generator.export_blank_template_pdf(template)
with open("questionnaire.pdf", "wb") as f:
    f.write(pdf_bytes)

# Export to JSON
json_str = generator.export_blank_template_json(template)
with open("questionnaire.json", "w") as f:
    f.write(json_str)

# Export to YAML
yaml_str = generator.export_blank_template_yaml(template)
with open("questionnaire.yaml", "w") as f:
    f.write(yaml_str)
```

## Template Structure

### Excel Template

The Excel template contains 7 worksheets:

1. **Instructions**: How to complete the questionnaire
2. **Metadata**: Template version, baseline version, export date, control count
3. **Controls**: All Moderate Baseline controls with descriptions
4. **Questions**: Discovery questions organized by control with blank response fields
5. **Framework Mappings**: NIST CSF, GLBA, SOX, FFIEC mappings
6. **AWS Hints**: AWS Config rules, Security Hub controls, Control Tower IDs
7. **Evidence**: Blank evidence fields for each control

### CSV Template

The CSV template includes 6 files:

- `controls.csv`: Control details
- `questions.csv`: Questions with blank response fields
- `mappings.csv`: Framework mappings
- `aws_hints.csv`: AWS control hints
- `metadata.csv`: Template metadata
- `evidence.csv`: Blank evidence fields

### PDF Template

The PDF template includes:

- Title page with metadata
- Instructions section
- Controls organized by family
- Questions and blank response fields for each control
- Blank evidence fields for each control

### JSON/YAML Templates

Structured data format with:

- Metadata object
- Controls array
- Questions object (keyed by control_id)
- Framework mappings object (keyed by control_id)
- AWS hints object (keyed by control_id)
- Evidence object with blank fields (keyed by control_id)

## Data Models

### Core Models

- **Control**: NIST 800-53 security control
- **DiscoveryQuestion**: Assessment question for a control
- **FrameworkMappings**: Cross-framework relationships
- **BlankQuestionnaireTemplate**: Complete template with all data
- **TemplateMetadata**: Template version and metadata

### Framework Mapping Models

- **NISTCSFMapping**: NIST Cybersecurity Framework mapping
- **GLBAMapping**: GLBA requirement mapping
- **SOXMapping**: SOX requirement mapping
- **FFIECMapping**: FFIEC requirement mapping
- **AWSControl**: AWS control from MCP server
- **ManagedControls**: AWS Config, Security Hub, Control Tower IDs

## Error Handling

The tool provides comprehensive error handling:

- **TemplateNotReadyError**: Template export attempted before data loaded
- **TemplateGenerationError**: General template generation failure
- **ExcelGenerationError**: Excel-specific generation failure
- **PDFGenerationError**: PDF-specific generation failure

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=compliance_discovery --cov-report=html

# Run specific test file
pytest tests/unit/test_template_export.py

# Run property-based tests
pytest tests/property/
```

## Requirements

- Python 3.8+
- openpyxl (Excel generation)
- reportlab (PDF generation)
- PyYAML (YAML support)
- requests (HTTP requests)
- pytest (testing)
- hypothesis (property-based testing)

## Architecture

The system follows a modular design:

1. **NIST 800-53 Parser**: Retrieves and parses OSCAL Moderate Baseline profile
2. **Discovery Question Generator**: Creates assessment questions
3. **Framework Mapper**: Manages cross-framework relationships
4. **Session Manager**: Orchestrates discovery sessions
5. **Export Generator**: Produces templates and session reports

## AWS Control Integration

The tool integrates with the compass-control-guides MCP server for real-time AWS control mappings:

- Search AWS Control Guides
- Get specific control details
- Map NIST controls to AWS controls
- Reverse lookup from AWS to NIST

When MCP is unavailable, templates include a note about missing AWS hints.

## Template Versioning

Templates use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking format changes
- **MINOR**: New fields or features
- **PATCH**: Bug fixes

Current version: 1.0.0

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass
5. Follow PEP 8 style guidelines

## License

[Add license information]

## Support

For questions or issues, contact the compliance team or AWS solutions architect.

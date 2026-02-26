#!/usr/bin/env python3
"""
Script to integrate all new control family questions into control_questions.py
"""

import re

# Read the new questions file
with open('add_all_remaining_families.py', 'r') as f:
    content = f.read()

# Extract just the questions dictionary content
match = re.search(r'NEW_CONTROL_QUESTIONS = """(.+?)"""', content, re.DOTALL)
if not match:
    print("ERROR: Could not find NEW_CONTROL_QUESTIONS in file")
    exit(1)

new_questions = match.group(1).strip()

# Read the existing control_questions.py
with open('compliance_discovery/control_questions.py', 'r') as f:
    existing_content = f.read()

# Find the position to insert (before the closing brace of CONTROL_QUESTIONS)
# Look for the last control (ra-5) and insert after it
insert_marker = """    'ra-5': [
        {
            'type': 'scanning_frequency',
            'question': 'How often are AWS resources scanned for vulnerabilities (continuous, weekly, monthly)? Are you using AWS Inspector for EC2, Lambda, and ECR scanning?',
        },
        {
            'type': 'scan_coverage',
            'question': 'What is scanned (EC2 instances, container images, Lambda functions, application code, infrastructure as code)? Are third-party dependencies analyzed?',
        },
        {
            'type': 'vulnerability_remediation',
            'question': 'What is your SLA for remediating vulnerabilities (critical: 7 days, high: 30 days, medium: 90 days)? How are exceptions handled, and who approves them?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates RA-5 compliance in AWS? Provide: AWS Config compliance reports for INSPECTOR_ENABLED, ECR_PRIVATE_IMAGE_SCANNING_ENABLED, EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK; Security Hub findings for ECR.1, SSM.2; Control Tower compliance status for SH.ECR.1, SH.SSM.2; Configuration screenshots from AWS Systems Manager, Amazon Elastic Container Registry, Amazon Inspector; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
}"""

if insert_marker not in existing_content:
    print("ERROR: Could not find insertion point in control_questions.py")
    exit(1)

# Replace the closing brace with new questions + closing brace
new_content = existing_content.replace(
    insert_marker,
    insert_marker[:-1] + new_questions + "\n}"
)

# Write the updated content
with open('compliance_discovery/control_questions.py', 'w') as f:
    f.write(new_content)

print("✓ Successfully integrated all new control family questions!")
print("\nAdded questions for control families:")
print("  - CA (Assessment, Authorization, and Monitoring): 7 controls")
print("  - SA (System and Services Acquisition): 11 controls")
print("  - PS (Personnel Security): 9 controls")
print("  - MA (Maintenance): 6 controls")
print("  - MP (Media Protection): 8 controls")
print("  - PM (Program Management): 16 controls")
print("  - PT (PII Processing and Transparency): 8 controls")
print("  - SR (Supply Chain Risk Management): 12 controls")
print("\nTotal new controls with AWS-specific questions: 77")

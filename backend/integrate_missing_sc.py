#!/usr/bin/env python3
"""
Script to integrate missing SC controls into control_questions.py
"""

import re

# Read the missing SC questions
with open('add_missing_sc_controls.py', 'r') as f:
    content = f.read()

# Extract the questions
match = re.search(r'MISSING_SC_QUESTIONS = """(.+?)"""', content, re.DOTALL)
if not match:
    print("ERROR: Could not find MISSING_SC_QUESTIONS")
    exit(1)

missing_questions = match.group(1).strip()

# Read existing control_questions.py
with open('compliance_discovery/control_questions.py', 'r') as f:
    existing_content = f.read()

# Find the SC section and insert the missing controls
# We'll insert after sc-1 and before sc-7
insert_point = """    'sc-1': [
        {
            'type': 'encryption_requirements',
            'question': 'What encryption requirements are documented in your policy (TLS 1.2+ for data in transit, KMS encryption for data at rest, S3 bucket encryption)? Are these enforced via SCPs or Config rules?',
        },
        {
            'type': 'network_architecture',
            'question': 'What network security requirements are mandated (VPC isolation, private subnets for workloads, no direct internet access for databases)? How is compliance verified?',
        },
        {
            'type': 'security_services',
            'question': 'What AWS security services are required (GuardDuty, Security Hub, WAF for public endpoints)? Are these enabled across all accounts?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-1 compliance in AWS? Provide: AWS Config compliance reports for DYNAMODB_TABLE_ENCRYPTED_KMS, S3_DEFAULT_ENCRYPTION_KMS, RDS_STORAGE_ENCRYPTED; Security Hub findings for DynamoDB.1, S3.4, RDS.3; Control Tower compliance status for CONFIG.DYNAMODB.DT.4, SH.RDS.3; Configuration screenshots from AWS Config, AWS Key Management Service, AWS Organizations; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],"""

if insert_point not in existing_content:
    print("ERROR: Could not find insertion point")
    exit(1)

# Insert the missing questions after sc-1
new_content = existing_content.replace(
    insert_point,
    insert_point + "\n" + missing_questions
)

# Write back
with open('compliance_discovery/control_questions.py', 'w') as f:
    f.write(new_content)

print("✓ Successfully integrated missing SC controls!")
print("\nAdded SC controls:")
print("  SC-2: Separation of System and User Functionality")
print("  SC-4: Information in Shared System Resources")
print("  SC-5: Denial-of-service Protection")
print("  SC-10: Network Disconnect")
print("  SC-15: Collaborative Computing Devices")
print("  SC-17: Public Key Infrastructure Certificates")
print("  SC-18: Mobile Code")
print("  SC-22: Architecture and Provisioning for Name/Address Resolution")
print("  SC-23: Session Authenticity")
print("  SC-39: Process Isolation")
print("\nTotal SC controls with questions: 18 (was 8, added 10)")

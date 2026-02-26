#!/usr/bin/env python3
"""
Add AWS implementation data for medium-priority NIST 800-53 controls.
These controls already have custom implementation questions but lack AWS-specific data.
"""

import json
from pathlib import Path
from datetime import datetime

# Medium-priority controls to add AWS data for
CONTROLS_TO_ADD = {
    'ac-3': {
        'title': 'Access Enforcement',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000052',
                'title': 'Configure least privilege access policies in AWS Identity and Access Management (IAM)',
                'description': 'Ensure that access policy permissions explicitly restrict the use of wildcards "*" and "allow all" in AWS IAM in order to enforce least privilege access and prevent unintended or unauthorized access to resources.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': ['IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS'],
                'security_hub_controls': ['IAM.21'],
                'control_tower_ids': ['SH.IAM.21'],
                'frameworks': ['NIST-SP-800-53-r5', 'PCI-DSS-v4.0', 'SSAE-18-SOC-2-Oct-2023']
            },
            {
                'control_id': 'AWS-CG-0000198',
                'title': 'Block public access to Amazon S3 buckets',
                'description': 'Configure Amazon S3 to block public access to S3 buckets in order to protect data from unauthorized access.',
                'services': ['Amazon S3'],
                'config_rules': ['S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS', 'S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED', 'S3_BUCKET_PUBLIC_READ_PROHIBITED'],
                'security_hub_controls': ['S3.1', 'S3.2', 'S3.3', 'S3.8'],
                'control_tower_ids': ['AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC', 'CT.S3.PR.1', 'SH.S3.1'],
                'frameworks': ['NIST-SP-800-53-r5', 'PCI-DSS-v4.0']
            },
            {
                'control_id': 'AWS-CG-0000224',
                'title': 'Disable public access to Amazon Elastic Kubernetes Service (EKS) endpoints',
                'description': 'Disable public access to Amazon EKS endpoints in order to avoid unintentional exposure and access to the cluster.',
                'services': ['Amazon Elastic Kubernetes Service'],
                'config_rules': ['EKS_ENDPOINT_NO_PUBLIC_ACCESS'],
                'security_hub_controls': ['EKS.1'],
                'control_tower_ids': ['AWS-GR_EKS_ENDPOINT_NO_PUBLIC_ACCESS', 'SH.EKS.1'],
                'frameworks': ['PCI-DSS-v4.0']
            }
        ]
    },
    'ia-2': {
        'title': 'Identification and Authentication (Organizational Users)',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000138',
                'title': 'Enable MFA for AWS Identity and Access Management (IAM) users that have a console password',
                'description': 'Enable MFA for IAM users that have a console password in order to strengthen user authentication.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': ['MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS'],
                'security_hub_controls': ['IAM.5'],
                'control_tower_ids': ['AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS', 'SH.IAM.5'],
                'frameworks': ['NIST-SP-800-53-r5', 'PCI-DSS-v4.0', 'SSAE-18-SOC-2-Oct-2023']
            },
            {
                'control_id': 'AWS-CG-0000187',
                'title': 'Configure Multi-Factor Authentication (MFA) for AWS Identity and Access Management (IAM) users',
                'description': 'Configure MFA for IAM users to protect resources from unauthorized access.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': ['IAM_USER_MFA_ENABLED'],
                'security_hub_controls': ['IAM.19'],
                'control_tower_ids': ['AWS-GR_IAM_USER_MFA_ENABLED'],
                'frameworks': ['SSAE-18-SOC-2-Oct-2023', 'PCI-DSS-v4.0']
            },
            {
                'control_id': 'AWS-CG-0000189',
                'title': 'Enable MFA for the AWS root account',
                'description': 'Enable MFA for the root account to add an extra layer of protection for the most privileged account.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': ['ROOT_ACCOUNT_MFA_ENABLED'],
                'security_hub_controls': ['IAM.6'],
                'control_tower_ids': ['AWS-GR_ROOT_ACCOUNT_MFA_ENABLED', 'SH.IAM.6'],
                'frameworks': ['NIST-SP-800-53-r5', 'PCI-DSS-v4.0']
            }
        ]
    },
    'ir-4': {
        'title': 'Incident Handling',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000367',
                'title': 'Enable Amazon GuardDuty for threat detection',
                'description': 'Enable GuardDuty to continuously monitor for malicious activity and unauthorized behavior to protect AWS accounts, workloads, and data.',
                'services': ['Amazon GuardDuty'],
                'config_rules': ['GUARDDUTY_ENABLED_CENTRALIZED', 'GUARDDUTY_NON_ARCHIVED_FINDINGS'],
                'security_hub_controls': ['GuardDuty.1'],
                'control_tower_ids': ['CONFIG.GUARDDUTY.DT.1', 'SH.GuardDuty.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000368',
                'title': 'Enable AWS Security Hub for centralized security findings',
                'description': 'Enable Security Hub to aggregate, organize, and prioritize security findings from multiple AWS services and third-party products.',
                'services': ['AWS Security Hub'],
                'config_rules': ['SECURITYHUB_ENABLED'],
                'security_hub_controls': [],
                'control_tower_ids': ['CONFIG.SECURITYHUB.DT.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000369',
                'title': 'Configure CloudWatch alarms for security events',
                'description': 'Configure CloudWatch alarms to detect and alert on security-relevant events for rapid incident response.',
                'services': ['Amazon CloudWatch'],
                'config_rules': ['CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK'],
                'security_hub_controls': ['CloudWatch.17'],
                'control_tower_ids': ['CONFIG.CLOUDWATCH.DT.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'ra-5': {
        'title': 'Vulnerability Monitoring and Scanning',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000370',
                'title': 'Enable Amazon Inspector for vulnerability scanning',
                'description': 'Enable Inspector to automatically discover workloads and continuously scan for software vulnerabilities and unintended network exposure.',
                'services': ['Amazon Inspector'],
                'config_rules': ['INSPECTOR_ENABLED'],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000371',
                'title': 'Enable ECR image scanning for container vulnerabilities',
                'description': 'Enable ECR image scanning to identify software vulnerabilities in container images.',
                'services': ['Amazon Elastic Container Registry'],
                'config_rules': ['ECR_PRIVATE_IMAGE_SCANNING_ENABLED'],
                'security_hub_controls': ['ECR.1'],
                'control_tower_ids': ['SH.ECR.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000372',
                'title': 'Configure Systems Manager for patch compliance',
                'description': 'Use Systems Manager Patch Manager to automate patching and track patch compliance across EC2 instances.',
                'services': ['AWS Systems Manager'],
                'config_rules': ['EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK'],
                'security_hub_controls': ['SSM.2'],
                'control_tower_ids': ['SH.SSM.2'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'si-2': {
        'title': 'Flaw Remediation',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000373',
                'title': 'Automate patching with Systems Manager Patch Manager',
                'description': 'Use Systems Manager Patch Manager to automate the process of patching managed instances with security-related updates.',
                'services': ['AWS Systems Manager'],
                'config_rules': ['EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK'],
                'security_hub_controls': ['SSM.2'],
                'control_tower_ids': ['SH.SSM.2'],
                'frameworks': ['NIST-SP-800-53-r5', 'PCI-DSS-v4.0']
            },
            {
                'control_id': 'AWS-CG-0000374',
                'title': 'Enable automatic minor version upgrades for RDS',
                'description': 'Enable automatic minor version upgrades for RDS database instances to ensure timely application of security patches.',
                'services': ['Amazon RDS'],
                'config_rules': ['RDS_AUTOMATIC_MINOR_VERSION_UPGRADE_ENABLED'],
                'security_hub_controls': ['RDS.13'],
                'control_tower_ids': ['SH.RDS.13'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000375',
                'title': 'Use latest Lambda runtime versions',
                'description': 'Ensure Lambda functions use the latest runtime versions to benefit from security patches and improvements.',
                'services': ['AWS Lambda'],
                'config_rules': ['LAMBDA_FUNCTION_SETTINGS_CHECK'],
                'security_hub_controls': ['Lambda.2'],
                'control_tower_ids': ['SH.Lambda.2'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    }
}


def load_existing_data():
    """Load existing AWS controls data."""
    data_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    with open(data_file, 'r') as f:
        return json.load(f)


def save_data(data):
    """Save updated AWS controls data."""
    data_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    print("="*80)
    print("ADDING MEDIUM-PRIORITY AWS CONTROLS")
    print("="*80)
    print()
    
    # Load existing data
    data = load_existing_data()
    print(f"Current controls: {data['metadata']['total_controls_mapped']}")
    print()
    
    # Add new controls
    added_count = 0
    for control_id, control_data in CONTROLS_TO_ADD.items():
        print(f"Adding {control_id.upper()}: {control_data['title']}")
        print(f"  AWS controls: {len(control_data['aws_controls'])}")
        
        data['controls'][control_id] = control_data['aws_controls']
        added_count += 1
    
    # Update metadata
    data['metadata']['total_controls_mapped'] = len(data['controls'])
    data['metadata']['export_date'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Save
    save_data(data)
    
    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Controls added: {added_count}")
    print(f"Total controls now: {data['metadata']['total_controls_mapped']}")
    print()
    print("✓ AWS controls data updated successfully!")
    print()
    print("NEXT STEPS:")
    print("1. Run improve_evidence_questions.py to generate evidence questions")
    print("2. Add evidence questions to control_questions.py")
    print("3. Test with sample questionnaire")


if __name__ == '__main__':
    main()

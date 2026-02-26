#!/usr/bin/env python3
"""
Add AWS implementation data for remaining medium-priority NIST 800-53 controls.
Focuses on controls with AWS-specific implementation potential.
"""

import json
from pathlib import Path
from datetime import datetime

# Remaining controls to add AWS data for
CONTROLS_TO_ADD = {
    'sc-20': {
        'title': 'Secure Name/Address Resolution Service (Authoritative Source)',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000779',
                'title': 'Route 53 Hosted Zones Must Have Tags',
                'description': 'Monitors Amazon Route 53 hosted zones to ensure they have at least one tag applied for resource management and tracking.',
                'services': ['Amazon Route 53'],
                'config_rules': ['ROUTE53_HOSTED_ZONE_TAGGED'],
                'security_hub_controls': [],
                'control_tower_ids': ['CONFIG.ROUTE53.DT.2'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000780',
                'title': 'Enable DNSSEC signing for Route 53 hosted zones',
                'description': 'Enable DNSSEC signing for Route 53 public hosted zones to provide authenticated DNS responses and prevent DNS spoofing attacks.',
                'services': ['Amazon Route 53'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000781',
                'title': 'Configure Route 53 query logging',
                'description': 'Enable query logging for Route 53 hosted zones to monitor DNS queries and detect potential security issues.',
                'services': ['Amazon Route 53'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'sc-21': {
        'title': 'Secure Name/Address Resolution Service (Recursive or Caching Resolver)',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000782',
                'title': 'Enable Route 53 Resolver DNS Firewall',
                'description': 'Enable Route 53 Resolver DNS Firewall to filter and block DNS queries to known malicious domains.',
                'services': ['Amazon Route 53'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000783',
                'title': 'Configure Route 53 Resolver DNSSEC validation',
                'description': 'Enable DNSSEC validation on Route 53 Resolver to validate DNS responses and prevent DNS spoofing.',
                'services': ['Amazon Route 53'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000784',
                'title': 'Enable GuardDuty DNS protection',
                'description': 'Enable GuardDuty to monitor DNS queries for malicious activity and potential data exfiltration attempts.',
                'services': ['Amazon GuardDuty'],
                'config_rules': ['GUARDDUTY_ENABLED_CENTRALIZED'],
                'security_hub_controls': ['GuardDuty.1'],
                'control_tower_ids': ['SH.GuardDuty.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'ac-1': {
        'title': 'Access Control Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000785',
                'title': 'Document IAM policies and procedures',
                'description': 'Maintain documented access control policies that define IAM user management, role-based access, and least privilege principles.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000786',
                'title': 'Use AWS Organizations for policy enforcement',
                'description': 'Implement Service Control Policies (SCPs) in AWS Organizations to enforce access control policies across all accounts.',
                'services': ['AWS Organizations'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000787',
                'title': 'Review IAM Access Analyzer findings',
                'description': 'Regularly review IAM Access Analyzer findings to identify unintended access to resources and ensure policy compliance.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'au-1': {
        'title': 'Audit and Accountability Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000788',
                'title': 'Document audit logging policy',
                'description': 'Maintain documented audit policy that defines CloudTrail requirements, log retention, and review procedures.',
                'services': ['AWS CloudTrail'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000789',
                'title': 'Centralize logs with AWS Organizations',
                'description': 'Use AWS Organizations to centralize CloudTrail logs from all accounts into a dedicated logging account.',
                'services': ['AWS CloudTrail', 'AWS Organizations'],
                'config_rules': ['CLOUDTRAIL_SECURITY_TRAIL_ENABLED'],
                'security_hub_controls': ['CloudTrail.3'],
                'control_tower_ids': ['CONFIG.CLOUDTRAIL.DT.6'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000790',
                'title': 'Implement log retention policies',
                'description': 'Configure CloudWatch Logs retention periods and S3 lifecycle policies to meet audit log retention requirements.',
                'services': ['Amazon CloudWatch Logs', 'Amazon S3'],
                'config_rules': ['CW_LOGGROUP_RETENTION_PERIOD_CHECK'],
                'security_hub_controls': ['CloudWatch.16'],
                'control_tower_ids': ['CONFIG.LOGS.DT.2'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'cm-1': {
        'title': 'Configuration Management Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000791',
                'title': 'Document configuration management policy',
                'description': 'Maintain documented configuration management policy requiring Infrastructure as Code and AWS Config for compliance monitoring.',
                'services': ['AWS Config'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000792',
                'title': 'Enable AWS Config in all regions',
                'description': 'Enable AWS Config in all regions to track configuration changes and maintain configuration history.',
                'services': ['AWS Config'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': ['AWS-GR_CONFIG_ENABLED'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000793',
                'title': 'Use CloudFormation or Terraform for IaC',
                'description': 'Implement Infrastructure as Code using CloudFormation or Terraform to ensure consistent and auditable infrastructure deployments.',
                'services': ['AWS CloudFormation'],
                'config_rules': ['CLOUDFORMATION_STACK_NOTIFICATION_CHECK'],
                'security_hub_controls': ['CloudFormation.1'],
                'control_tower_ids': ['CONFIG.CLOUDFORMATION.DT.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'cp-1': {
        'title': 'Contingency Planning Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000794',
                'title': 'Document disaster recovery policy',
                'description': 'Maintain documented contingency planning policy that defines RTO/RPO requirements and AWS Backup strategies.',
                'services': ['AWS Backup'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000795',
                'title': 'Implement AWS Backup centralized management',
                'description': 'Use AWS Backup to centrally manage and automate backups across AWS services.',
                'services': ['AWS Backup'],
                'config_rules': ['BACKUP_RECOVERY_POINT_ENCRYPTED', 'BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK'],
                'security_hub_controls': ['Backup.1'],
                'control_tower_ids': ['BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000796',
                'title': 'Configure multi-region replication',
                'description': 'Implement cross-region replication for critical data using S3 replication, RDS read replicas, or DynamoDB global tables.',
                'services': ['Amazon S3', 'Amazon RDS', 'Amazon DynamoDB'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'ia-1': {
        'title': 'Identification and Authentication Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000797',
                'title': 'Document authentication policy',
                'description': 'Maintain documented authentication policy requiring MFA, password complexity, and federated access via SSO.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000798',
                'title': 'Implement IAM Identity Center for SSO',
                'description': 'Use AWS IAM Identity Center (formerly AWS SSO) to provide centralized authentication and federated access.',
                'services': ['AWS IAM Identity Center'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000799',
                'title': 'Enforce IAM password policy',
                'description': 'Configure IAM password policy with minimum length, complexity requirements, and rotation periods.',
                'services': ['AWS Identity and Access Management'],
                'config_rules': ['IAM_PASSWORD_POLICY'],
                'security_hub_controls': ['IAM.7', 'IAM.8', 'IAM.9', 'IAM.10', 'IAM.11'],
                'control_tower_ids': ['SH.IAM.7', 'SH.IAM.8'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'ir-1': {
        'title': 'Incident Response Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000800',
                'title': 'Document incident response policy',
                'description': 'Maintain documented incident response policy that defines AWS-specific incident handling procedures and escalation paths.',
                'services': ['AWS Security Hub'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000801',
                'title': 'Enable Security Hub for incident aggregation',
                'description': 'Use Security Hub to aggregate security findings from multiple AWS services for centralized incident detection.',
                'services': ['AWS Security Hub'],
                'config_rules': ['SECURITYHUB_ENABLED'],
                'security_hub_controls': [],
                'control_tower_ids': ['CONFIG.SECURITYHUB.DT.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000802',
                'title': 'Configure EventBridge for incident automation',
                'description': 'Use Amazon EventBridge to automate incident response actions based on Security Hub findings and GuardDuty alerts.',
                'services': ['Amazon EventBridge'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'ra-1': {
        'title': 'Risk Assessment Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000803',
                'title': 'Document risk assessment policy',
                'description': 'Maintain documented risk assessment policy that defines AWS security assessment procedures and risk acceptance criteria.',
                'services': ['AWS Security Hub'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000804',
                'title': 'Use Security Hub security standards',
                'description': 'Enable Security Hub security standards (AWS Foundational Security Best Practices, CIS AWS Foundations) for continuous risk assessment.',
                'services': ['AWS Security Hub'],
                'config_rules': ['SECURITYHUB_ENABLED'],
                'security_hub_controls': [],
                'control_tower_ids': ['CONFIG.SECURITYHUB.DT.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000805',
                'title': 'Review AWS Trusted Advisor findings',
                'description': 'Regularly review AWS Trusted Advisor security recommendations to identify and remediate security risks.',
                'services': ['AWS Trusted Advisor'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'sc-1': {
        'title': 'System and Communications Protection Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000806',
                'title': 'Document encryption policy',
                'description': 'Maintain documented encryption policy requiring TLS 1.2+ for data in transit and KMS encryption for data at rest.',
                'services': ['AWS Key Management Service'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000807',
                'title': 'Enforce encryption with SCPs',
                'description': 'Use Service Control Policies to enforce encryption requirements across all AWS accounts in the organization.',
                'services': ['AWS Organizations'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000808',
                'title': 'Monitor encryption compliance with Config',
                'description': 'Use AWS Config rules to continuously monitor encryption compliance for S3, EBS, RDS, and other services.',
                'services': ['AWS Config'],
                'config_rules': ['DYNAMODB_TABLE_ENCRYPTED_KMS', 'S3_DEFAULT_ENCRYPTION_KMS', 'RDS_STORAGE_ENCRYPTED'],
                'security_hub_controls': ['DynamoDB.1', 'S3.4', 'RDS.3'],
                'control_tower_ids': ['CONFIG.DYNAMODB.DT.4', 'SH.RDS.3'],
                'frameworks': ['NIST-SP-800-53-r5']
            }
        ]
    },
    'si-1': {
        'title': 'System and Information Integrity Policy and Procedures',
        'aws_controls': [
            {
                'control_id': 'AWS-CG-0000809',
                'title': 'Document security monitoring policy',
                'description': 'Maintain documented security monitoring policy that defines GuardDuty, Security Hub, and vulnerability scanning requirements.',
                'services': ['Amazon GuardDuty', 'AWS Security Hub'],
                'config_rules': [],
                'security_hub_controls': [],
                'control_tower_ids': [],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000810',
                'title': 'Enable GuardDuty in all regions',
                'description': 'Enable GuardDuty in all regions to continuously monitor for malicious activity and unauthorized behavior.',
                'services': ['Amazon GuardDuty'],
                'config_rules': ['GUARDDUTY_ENABLED_CENTRALIZED'],
                'security_hub_controls': ['GuardDuty.1'],
                'control_tower_ids': ['CONFIG.GUARDDUTY.DT.1', 'SH.GuardDuty.1'],
                'frameworks': ['NIST-SP-800-53-r5']
            },
            {
                'control_id': 'AWS-CG-0000811',
                'title': 'Enable Inspector for vulnerability scanning',
                'description': 'Enable Amazon Inspector to automatically scan EC2 instances, Lambda functions, and container images for vulnerabilities.',
                'services': ['Amazon Inspector'],
                'config_rules': ['INSPECTOR_ENABLED'],
                'security_hub_controls': [],
                'control_tower_ids': [],
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
    print("ADDING REMAINING MEDIUM-PRIORITY AWS CONTROLS")
    print("="*80)
    print()
    
    # Load existing data
    data = load_existing_data()
    print(f"Current controls: {data['metadata']['total_controls_mapped']}")
    print()
    
    # Add new controls
    added_count = 0
    total_aws_controls = 0
    for control_id, control_data in CONTROLS_TO_ADD.items():
        print(f"Adding {control_id.upper()}: {control_data['title']}")
        print(f"  AWS controls: {len(control_data['aws_controls'])}")
        
        data['controls'][control_id] = control_data['aws_controls']
        added_count += 1
        total_aws_controls += len(control_data['aws_controls'])
    
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
    print(f"AWS controls added: {total_aws_controls}")
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

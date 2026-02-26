"""Fallback AWS control mappings for common NIST controls.

Used when MCP server is unavailable or doesn't return results.
"""

from typing import Dict, List

# Controls that AWS is responsible for (physical/infrastructure)
AWS_RESPONSIBILITY_CONTROLS = [
    'pe-1', 'pe-2', 'pe-3', 'pe-4', 'pe-5', 'pe-6', 'pe-8', 'pe-9', 'pe-10',
    'pe-11', 'pe-12', 'pe-13', 'pe-14', 'pe-15', 'pe-16', 'pe-17', 'pe-18',
    'ma-2', 'ma-3', 'ma-4', 'ma-5', 'ma-6',  # Maintenance controls
]

# Controls with AWS managed services (shared responsibility)
AWS_MANAGED_CONTROLS: Dict[str, List[str]] = {
    # Access Control
    'ac-2': ['IAM User Management', 'AWS Organizations', 'AWS SSO'],
    'ac-3': ['IAM Policies', 'S3 Bucket Policies', 'Resource-based Policies'],
    'ac-4': ['Security Groups', 'NACLs', 'VPC Flow Logs'],
    'ac-6': ['IAM Least Privilege', 'Service Control Policies'],
    'ac-17': ['VPN', 'Direct Connect', 'AWS Client VPN'],
    
    # Audit and Accountability
    'au-2': ['CloudTrail', 'CloudWatch Logs', 'VPC Flow Logs'],
    'au-3': ['CloudTrail', 'CloudWatch Logs'],
    'au-4': ['CloudWatch Logs', 'S3 for log storage'],
    'au-6': ['CloudWatch Insights', 'Athena', 'Security Hub'],
    'au-9': ['CloudTrail Log File Validation', 'S3 Object Lock'],
    'au-11': ['S3 Lifecycle Policies', 'Glacier'],
    'au-12': ['CloudTrail', 'CloudWatch', 'Config'],
    
    # Configuration Management
    'cm-2': ['AWS Config', 'Systems Manager', 'EC2 Image Builder'],
    'cm-3': ['AWS Config', 'CloudFormation', 'Service Catalog'],
    'cm-6': ['AWS Config Rules', 'Systems Manager'],
    'cm-7': ['Security Groups', 'Systems Manager', 'Inspector'],
    'cm-8': ['AWS Config', 'Systems Manager Inventory', 'Resource Groups'],
    
    # Contingency Planning
    'cp-6': ['S3 Cross-Region Replication', 'Multi-Region Architecture'],
    'cp-7': ['Multi-Region Deployment', 'Route 53'],
    'cp-9': ['EBS Snapshots', 'RDS Automated Backups', 'S3 Versioning', 'AWS Backup'],
    'cp-10': ['CloudFormation', 'Elastic Disaster Recovery'],
    
    # Identification and Authentication
    'ia-2': ['IAM', 'Cognito', 'AWS SSO', 'MFA'],
    'ia-3': ['Device Certificates', 'IoT Device Management'],
    'ia-4': ['IAM', 'AWS Organizations'],
    'ia-5': ['IAM Password Policy', 'Secrets Manager', 'KMS'],
    'ia-8': ['IAM Roles for Cross-Account', 'Cognito'],
    
    # Incident Response
    'ir-4': ['GuardDuty', 'Security Hub', 'Detective'],
    'ir-5': ['CloudWatch Events', 'SNS', 'Systems Manager'],
    'ir-6': ['Security Hub', 'GuardDuty findings'],
    
    # System and Communications Protection
    'sc-7': ['Security Groups', 'NACLs', 'WAF', 'Shield'],
    'sc-8': ['TLS/SSL', 'VPN', 'Certificate Manager'],
    'sc-12': ['KMS', 'CloudHSM'],
    'sc-13': ['KMS', 'CloudHSM', 'Encryption SDK'],
    'sc-28': ['EBS Encryption', 'S3 Encryption', 'RDS Encryption'],
    
    # System and Information Integrity
    'si-2': ['Systems Manager Patch Manager', 'Inspector'],
    'si-3': ['GuardDuty', 'Macie'],
    'si-4': ['GuardDuty', 'Security Hub', 'VPC Flow Logs', 'CloudWatch'],
    'si-7': ['CloudTrail Log Validation', 'Code Signing'],
    
    # Risk Assessment
    'ra-5': ['Inspector', 'Security Hub', 'GuardDuty'],
}


def get_aws_responsibility(control_id: str) -> str:
    """Determine AWS shared responsibility for a control.
    
    Args:
        control_id: NIST control ID (e.g., "AC-2")
        
    Returns:
        'aws', 'shared', or 'customer'
    """
    control_lower = control_id.lower()
    
    if control_lower in AWS_RESPONSIBILITY_CONTROLS:
        return 'aws'
    elif control_lower in AWS_MANAGED_CONTROLS:
        return 'shared'
    else:
        return 'customer'


def get_aws_services(control_id: str) -> List[str]:
    """Get AWS services that help implement a control.
    
    Args:
        control_id: NIST control ID
        
    Returns:
        List of AWS service names
    """
    return AWS_MANAGED_CONTROLS.get(control_id.lower(), [])

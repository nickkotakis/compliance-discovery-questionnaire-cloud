"""AWS Shared Responsibility Model mappings for NIST 800-53 controls.

This module defines which NIST controls fall under AWS responsibility, shared responsibility,
or customer responsibility based on the AWS Shared Responsibility Model.

SOURCES & RATIONALE:
-------------------
1. AWS Shared Responsibility Model: https://aws.amazon.com/compliance/shared-responsibility-model/
2. AWS Compliance Programs: https://aws.amazon.com/compliance/programs/
3. AWS Artifact (Compliance Reports): Available in AWS Console
4. NIST 800-53 Control Families: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

RESPONSIBILITY CATEGORIES:
-------------------------
- AWS RESPONSIBILITY: Controls AWS implements for their infrastructure (data centers, hardware, 
  physical security, network infrastructure). Customers inherit this protection automatically.
  Evidence: AWS Artifact compliance reports (SOC, ISO, PCI, etc.)

- SHARED RESPONSIBILITY: Controls where AWS provides the tools/services, but customers must 
  configure and use them properly. AWS secures the platform, customers secure their workloads.
  Evidence: AWS service configurations + customer implementation documentation

- CUSTOMER RESPONSIBILITY: Controls customers must implement entirely within their applications,
  processes, or using third-party tools. AWS provides the infrastructure, customers handle the rest.
  Evidence: Customer documentation, policies, and implementation artifacts

CUSTOMIZATION:
--------------
Organizations can override these default mappings using the responsibility_overrides.json file
to reflect their specific AWS architecture and compliance requirements.
"""

from typing import Dict, List

# ============================================================================
# AWS RESPONSIBILITY CONTROLS
# ============================================================================
# RATIONALE: AWS is responsible for "security OF the cloud" - the physical
# infrastructure, hardware, networking, and facilities that run AWS services.
# 
# SOURCE: AWS Shared Responsibility Model
# https://aws.amazon.com/compliance/shared-responsibility-model/
#
# EVIDENCE: AWS Artifact compliance reports demonstrate AWS implementation
# of these controls. Customers can download SOC 2, ISO 27001, PCI DSS, and
# other reports showing AWS data center security measures.
# ============================================================================

AWS_RESPONSIBILITY_CONTROLS = [
    # Physical and Environmental Protection (PE family)
    # AWS manages all physical security for their data centers
    'pe-1',   # Physical and Environmental Protection Policy
    'pe-2',   # Physical Access Authorizations
    'pe-3',   # Physical Access Control
    'pe-4',   # Access Control for Transmission Medium
    'pe-5',   # Access Control for Output Devices
    'pe-6',   # Monitoring Physical Access
    'pe-8',   # Visitor Access Records
    'pe-9',   # Power Equipment and Cabling
    'pe-10',  # Emergency Shutoff
    'pe-11',  # Emergency Power
    'pe-12',  # Emergency Lighting
    'pe-13',  # Fire Protection
    'pe-14',  # Temperature and Humidity Controls
    'pe-15',  # Water Damage Protection
    'pe-16',  # Delivery and Removal
    'pe-17',  # Alternate Work Site (for AWS employees)
    'pe-18',  # Location of System Components
    
    # Maintenance (MA family)
    # AWS manages hardware maintenance for their infrastructure
    'ma-2',   # Controlled Maintenance
    'ma-3',   # Maintenance Tools
    'ma-4',   # Nonlocal Maintenance
    'ma-5',   # Maintenance Personnel
    'ma-6',   # Timely Maintenance
]

# ============================================================================
# SHARED RESPONSIBILITY CONTROLS
# ============================================================================
# RATIONALE: AWS provides managed services and tools, but customers must
# configure and use them properly. This is "security IN the cloud."
#
# SOURCE: AWS service documentation and compliance guidance
# - AWS Config: https://aws.amazon.com/config/
# - AWS CloudTrail: https://aws.amazon.com/cloudtrail/
# - AWS Security Hub: https://aws.amazon.com/security-hub/
# - AWS IAM: https://aws.amazon.com/iam/
#
# EVIDENCE: Combination of AWS Artifact reports (showing AWS platform security)
# + customer configuration screenshots/exports (showing proper implementation)
# ============================================================================

# Controls with AWS managed services (shared responsibility)
AWS_MANAGED_CONTROLS: Dict[str, List[str]] = {
    # ========================================================================
    # ACCESS CONTROL (AC family)
    # AWS provides IAM, Organizations, and access control services
    # Customers must configure policies and manage user access
    # ========================================================================
    'ac-2': ['IAM User Management', 'AWS Organizations', 'AWS SSO'],
    'ac-3': ['IAM Policies', 'S3 Bucket Policies', 'Resource-based Policies'],
    'ac-4': ['Security Groups', 'NACLs', 'VPC Flow Logs'],
    'ac-6': ['IAM Least Privilege', 'Service Control Policies'],
    'ac-17': ['VPN', 'Direct Connect', 'AWS Client VPN'],
    
    # ========================================================================
    # AUDIT AND ACCOUNTABILITY (AU family)
    # AWS provides logging services (CloudTrail, CloudWatch, Config)
    # Customers must enable, configure, and monitor these services
    # ========================================================================
    'au-2': ['CloudTrail', 'CloudWatch Logs', 'VPC Flow Logs'],
    'au-3': ['CloudTrail', 'CloudWatch Logs'],
    'au-4': ['CloudWatch Logs', 'S3 for log storage'],
    'au-6': ['CloudWatch Insights', 'Athena', 'Security Hub'],
    'au-9': ['CloudTrail Log File Validation', 'S3 Object Lock'],
    'au-11': ['S3 Lifecycle Policies', 'Glacier'],
    'au-12': ['CloudTrail', 'CloudWatch', 'Config'],
    
    # ========================================================================
    # CONFIGURATION MANAGEMENT (CM family)
    # AWS provides Config, Systems Manager, and IaC tools
    # Customers must define baselines and manage configurations
    # ========================================================================
    'cm-2': ['AWS Config', 'Systems Manager', 'EC2 Image Builder'],
    'cm-3': ['AWS Config', 'CloudFormation', 'Service Catalog'],
    'cm-6': ['AWS Config Rules', 'Systems Manager'],
    'cm-7': ['Security Groups', 'Systems Manager', 'Inspector'],
    'cm-8': ['AWS Config', 'Systems Manager Inventory', 'Resource Groups'],
    
    # ========================================================================
    # CONTINGENCY PLANNING (CP family)
    # AWS provides backup services and multi-region capabilities
    # Customers must design DR architecture and test recovery procedures
    # ========================================================================
    'cp-6': ['S3 Cross-Region Replication', 'Multi-Region Architecture'],
    'cp-7': ['Multi-Region Deployment', 'Route 53'],
    'cp-9': ['EBS Snapshots', 'RDS Automated Backups', 'S3 Versioning', 'AWS Backup'],
    'cp-10': ['CloudFormation', 'Elastic Disaster Recovery'],
    
    # ========================================================================
    # IDENTIFICATION AND AUTHENTICATION (IA family)
    # AWS provides IAM, Cognito, and authentication services
    # Customers must configure MFA, password policies, and user management
    # ========================================================================
    'ia-2': ['IAM', 'Cognito', 'AWS SSO', 'MFA'],
    'ia-3': ['Device Certificates', 'IoT Device Management'],
    'ia-4': ['IAM', 'AWS Organizations'],
    'ia-5': ['IAM Password Policy', 'Secrets Manager', 'KMS'],
    'ia-8': ['IAM Roles for Cross-Account', 'Cognito'],
    
    # ========================================================================
    # INCIDENT RESPONSE (IR family)
    # AWS provides GuardDuty, Security Hub, and Detective
    # Customers must configure alerting and define response procedures
    # ========================================================================
    'ir-4': ['GuardDuty', 'Security Hub', 'Detective'],
    'ir-5': ['CloudWatch Events', 'SNS', 'Systems Manager'],
    'ir-6': ['Security Hub', 'GuardDuty findings'],
    
    # ========================================================================
    # SYSTEM AND COMMUNICATIONS PROTECTION (SC family)
    # AWS provides encryption services, network security, and WAF
    # Customers must enable encryption and configure network controls
    # ========================================================================
    'sc-7': ['Security Groups', 'NACLs', 'WAF', 'Shield'],
    'sc-8': ['TLS/SSL', 'VPN', 'Certificate Manager'],
    'sc-12': ['KMS', 'CloudHSM'],
    'sc-13': ['KMS', 'CloudHSM', 'Encryption SDK'],
    'sc-28': ['EBS Encryption', 'S3 Encryption', 'RDS Encryption'],
    
    # ========================================================================
    # SYSTEM AND INFORMATION INTEGRITY (SI family)
    # AWS provides GuardDuty, Inspector, and Macie
    # Customers must enable scanning and respond to findings
    # ========================================================================
    'si-2': ['Systems Manager Patch Manager', 'Inspector'],
    'si-3': ['GuardDuty', 'Macie'],
    'si-4': ['GuardDuty', 'Security Hub', 'VPC Flow Logs', 'CloudWatch'],
    'si-7': ['CloudTrail Log Validation', 'Code Signing'],
    
    # ========================================================================
    # RISK ASSESSMENT (RA family)
    # AWS provides Inspector, Security Hub, and vulnerability scanning
    # Customers must run scans and remediate findings
    # ========================================================================
    'ra-5': ['Inspector', 'Security Hub', 'GuardDuty'],
}

# ============================================================================
# RESPONSIBILITY OVERRIDE SUPPORT
# ============================================================================
# Organizations can customize responsibility assignments by creating a
# responsibility_overrides.json file in the backend directory.
#
# Format:
# {
#   "control_id": "responsibility",  // "aws", "shared", or "customer"
#   "ac-1": "shared",  // Override AC-1 to shared responsibility
#   "pe-1": "customer"  // Override PE-1 to customer responsibility
# }
# ============================================================================

import json
import os
from pathlib import Path

def load_responsibility_overrides() -> Dict[str, str]:
    """Load responsibility overrides from JSON file if it exists.
    
    Returns:
        Dictionary mapping control IDs to responsibility values
    """
    override_file = Path(__file__).parent.parent / 'responsibility_overrides.json'
    
    if override_file.exists():
        try:
            with open(override_file, 'r') as f:
                overrides = json.load(f)
                print(f"Loaded {len(overrides)} responsibility overrides from {override_file}")
                return {k.lower(): v.lower() for k, v in overrides.items()}
        except Exception as e:
            print(f"Warning: Could not load responsibility overrides: {e}")
            return {}
    return {}

# Load overrides at module import
_RESPONSIBILITY_OVERRIDES = load_responsibility_overrides()


def get_aws_responsibility(control_id: str) -> str:
    """Determine AWS shared responsibility for a control.
    
    Checks for overrides first, then falls back to default mappings.
    
    Args:
        control_id: NIST control ID (e.g., "AC-2")
        
    Returns:
        'aws', 'shared', or 'customer'
    """
    control_lower = control_id.lower()
    
    # Check for override first
    if control_lower in _RESPONSIBILITY_OVERRIDES:
        override_value = _RESPONSIBILITY_OVERRIDES[control_lower]
        print(f"Using override for {control_id}: {override_value}")
        return override_value
    
    # Fall back to default mappings
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

"""Control-specific implementation questions for NIST 800-53 controls.

These questions focus on practical implementation details, specific safeguards,
and real-world processes rather than generic compliance questions.
"""

from typing import List, Dict

# Control-specific implementation questions
CONTROL_QUESTIONS = {
    # Physical and Environmental Protection
    'pe-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented physical and environmental protection policy? Where is it stored and when was it last reviewed?',
        },
        {
            'type': 'aws_acknowledgment',
            'question': 'Does your policy acknowledge that AWS is responsible for physical security of their data centers? Have you obtained AWS compliance reports from AWS Artifact to document this?',
        },
    ],
    'pe-4': [
        {
            'type': 'physical_safeguards',
            'question': 'Are network cables and communication lines housed in locked wiring closets or protected by conduits/cable trays? Describe the physical protection measures.',
        },
        {
            'type': 'unused_ports',
            'question': 'Are unused network jacks and ports secured or disconnected? How are inactive network connections managed?',
        },
    ],
    
    # Access Control
    'ac-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented access control policy covering your AWS environment? Where is it stored and when was it last reviewed?',
        },
        {
            'type': 'policy_scope',
            'question': 'Does your access control policy address IAM users, roles, resource policies, and the principle of least privilege in AWS?',
        },
    ],
    'ac-2': [
        {
            'type': 'account_lifecycle',
            'question': 'What is the process for creating, modifying, and disabling IAM users and roles in AWS? Who approves these actions and how quickly are they executed?',
        },
        {
            'type': 'account_review',
            'question': 'How often are AWS IAM users and roles reviewed for appropriateness? Are you using AWS IAM Access Analyzer or similar tools to identify unused access?',
        },
    ],
    'ac-3': [
        {
            'type': 'authorization_model',
            'question': 'How are IAM policies, resource policies, and SCPs used to enforce access control in AWS? Are you using attribute-based access control (ABAC) with tags?',
        },
        {
            'type': 'least_privilege',
            'question': 'How do you ensure least privilege in AWS? Are you using IAM Access Analyzer policy validation or AWS Access Advisor to identify excessive permissions?',
        },
    ],
    
    # Audit and Accountability
    'au-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented audit and accountability policy for AWS? Does it specify what events must be logged in CloudTrail and CloudWatch?',
        },
        {
            'type': 'log_retention',
            'question': 'Does your policy define log retention periods for CloudTrail, VPC Flow Logs, and application logs? How are these enforced?',
        },
    ],
    'au-2': [
        {
            'type': 'auditable_events',
            'question': 'What AWS events are being logged (API calls via CloudTrail, network traffic via VPC Flow Logs, application logs via CloudWatch)? How was this list determined?',
        },
        {
            'type': 'logging_coverage',
            'question': 'Is CloudTrail enabled in all regions and accounts? Are you using AWS Organizations to enforce CloudTrail across all accounts?',
        },
    ],
    
    # Configuration Management
    'cm-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented configuration management policy for AWS resources? Does it address Infrastructure as Code (IaC) and configuration drift?',
        },
        {
            'type': 'change_control',
            'question': 'Does your policy require all AWS infrastructure changes to go through version control (CloudFormation, Terraform) and approval processes?',
        },
    ],
    'cm-2': [
        {
            'type': 'baseline_configs',
            'question': 'Are baseline configurations documented for EC2 instances, RDS databases, and other AWS resources? Are you using AWS Config rules or custom policies to enforce these?',
        },
        {
            'type': 'config_verification',
            'question': 'How do you detect configuration drift in AWS? Are you using AWS Config, Systems Manager, or third-party tools to monitor compliance with baselines?',
        },
    ],
    
    # Identification and Authentication
    'ia-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented identification and authentication policy for AWS? Does it mandate MFA for privileged access?',
        },
        {
            'type': 'federation',
            'question': 'Does your policy address federated access to AWS (SSO, SAML)? Are you using AWS IAM Identity Center (formerly AWS SSO)?',
        },
    ],
    'ia-2': [
        {
            'type': 'authentication_methods',
            'question': 'Is MFA required for AWS console access, especially for privileged users? What percentage of IAM users have MFA enabled?',
        },
        {
            'type': 'password_policy',
            'question': 'What is your IAM password policy (length, complexity, rotation)? Are you enforcing it via AWS IAM password policy settings?',
        },
    ],
    
    # System and Communications Protection
    'sc-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented system and communications protection policy for AWS? Does it mandate encryption in transit and at rest?',
        },
        {
            'type': 'network_security',
            'question': 'Does your policy require VPC isolation, security groups, and network segmentation for AWS workloads?',
        },
    ],
    'sc-7': [
        {
            'type': 'network_segmentation',
            'question': 'How are your AWS VPCs segmented (public/private subnets, multiple VPCs)? Are you using security groups and NACLs to control traffic between segments?',
        },
        {
            'type': 'boundary_monitoring',
            'question': 'What tools monitor traffic at VPC boundaries (VPC Flow Logs, GuardDuty, third-party firewalls)? How are security alerts handled?',
        },
    ],
    
    # System and Information Integrity
    'si-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented system and information integrity policy for AWS? Does it address vulnerability scanning and patch management?',
        },
        {
            'type': 'malware_protection',
            'question': 'Does your policy require anti-malware protection for EC2 instances and container images? What tools are mandated?',
        },
    ],
    'si-2': [
        {
            'type': 'patch_process',
            'question': 'How are EC2 instances and container images patched? Are you using AWS Systems Manager Patch Manager or automated AMI/container rebuilds?',
        },
        {
            'type': 'vulnerability_scanning',
            'question': 'How often are AWS resources scanned for vulnerabilities? Are you using AWS Inspector, ECR image scanning, or third-party tools?',
        },
    ],
    
    # Contingency Planning
    'cp-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented contingency planning policy for AWS workloads? Does it address RTO/RPO requirements?',
        },
        {
            'type': 'disaster_recovery',
            'question': 'Does your policy require multi-region or multi-AZ deployments for critical workloads? Are backup and recovery procedures documented?',
        },
    ],
    'cp-9': [
        {
            'type': 'backup_scope',
            'question': 'What AWS resources are backed up (EBS snapshots, RDS automated backups, S3 versioning)? Are you using AWS Backup for centralized backup management?',
        },
        {
            'type': 'backup_testing',
            'question': 'How often are AWS backup restores tested? When was the last successful restore? Are backups encrypted and stored in a separate region?',
        },
    ],
    
    # Incident Response
    'ir-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented incident response policy for AWS security events? Does it define roles and escalation procedures?',
        },
        {
            'type': 'aws_integration',
            'question': 'Does your policy address how to respond to GuardDuty findings, Security Hub alerts, and CloudTrail anomalies?',
        },
    ],
    'ir-4': [
        {
            'type': 'incident_detection',
            'question': 'How are security incidents detected in AWS (GuardDuty, Security Hub, CloudWatch alarms)? What triggers an incident response?',
        },
        {
            'type': 'incident_procedures',
            'question': 'Are incident response runbooks documented for common AWS scenarios (compromised IAM credentials, S3 data exposure, EC2 compromise)? How often are they tested?',
        },
    ],
    
    # Planning
    'pl-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented security planning policy? Does it require security to be considered in AWS architecture decisions?',
        },
        {
            'type': 'aws_well_architected',
            'question': 'Do you use the AWS Well-Architected Framework for security planning? Are Well-Architected Reviews conducted for critical workloads?',
        },
    ],
    
    # Risk Assessment
    'ra-1': [
        {
            'type': 'policy_existence',
            'question': 'Does your organization have a documented risk assessment policy for AWS? How often are risk assessments conducted?',
        },
        {
            'type': 'aws_risks',
            'question': 'Does your risk assessment process address AWS-specific risks (misconfigurations, excessive permissions, public exposure)?',
        },
    ],
    'ra-5': [
        {
            'type': 'vulnerability_scanning',
            'question': 'How often are AWS resources scanned for vulnerabilities? Are you using AWS Inspector for EC2 and container scanning?',
        },
        {
            'type': 'remediation',
            'question': 'What is the process for remediating vulnerabilities found in AWS? Are critical vulnerabilities tracked and escalated?',
        },
    ],
}


def get_control_questions(control_id: str) -> List[Dict[str, str]]:
    """Get implementation-focused questions for a specific control.
    
    Args:
        control_id: NIST control ID (e.g., "AC-2" or "ac-2")
        
    Returns:
        List of question dictionaries with 'type' and 'question' keys
    """
    return CONTROL_QUESTIONS.get(control_id.lower(), [])


def has_custom_questions(control_id: str) -> bool:
    """Check if a control has custom implementation questions.
    
    Args:
        control_id: NIST control ID
        
    Returns:
        True if custom questions exist
    """
    return control_id.lower() in CONTROL_QUESTIONS

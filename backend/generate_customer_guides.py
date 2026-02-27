#!/usr/bin/env python3
"""Generate AWS implementation guides for customer responsibility controls.

This script creates practical AWS implementation guides for NIST 800-53 controls
that are customer responsibility, based on AWS best practices and services.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from compliance_discovery.nist_parser import NIST80053Parser
from compliance_discovery.aws_control_mapping import get_aws_responsibility


# AWS implementation guides for customer responsibility controls
CUSTOMER_CONTROL_GUIDES = {
    'ac-5': {
        'title': 'Separation of Duties',
        'description': 'Implement separation of duties using IAM roles and policies',
        'services': ['IAM', 'AWS Organizations', 'CloudTrail'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use IAM roles to separate administrative functions. Create distinct roles for different job functions (e.g., SecurityAdmin, DatabaseAdmin, NetworkAdmin). Use AWS Organizations SCPs to enforce separation at the organizational level. Monitor role usage with CloudTrail.'
    },
    'ac-7': {
        'title': 'Unsuccessful Logon Attempts',
        'description': 'Enforce account lockout after failed login attempts',
        'services': ['Cognito', 'IAM', 'CloudWatch', 'Lambda'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'For application users: Configure Cognito user pools with account lockout policies. For AWS Console: Use CloudWatch Events to detect failed console logins and trigger Lambda functions to disable IAM users after threshold. Implement custom authentication with lockout logic in your applications.'
    },
    'ac-8': {
        'title': 'System Use Notification',
        'description': 'Display system use notification messages',
        'services': ['Cognito', 'API Gateway', 'CloudFront'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Display banner messages in your applications before authentication. Use Cognito pre-authentication Lambda triggers to present terms of use. Add consent banners to web applications served through CloudFront. Include usage notifications in API Gateway responses.'
    },
    'ac-11': {
        'title': 'Session Lock',
        'description': 'Implement automatic session lock after inactivity',
        'services': ['Cognito', 'Application Load Balancer', 'Lambda'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Configure Cognito token expiration and refresh token policies. Implement session timeout in your application code. Use ALB session stickiness with appropriate timeout values. For web apps, implement client-side session timeout with automatic logout.'
    },
    'ac-12': {
        'title': 'Session Termination',
        'description': 'Automatically terminate sessions after defined conditions',
        'services': ['Cognito', 'Lambda', 'DynamoDB'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Set Cognito access token lifetime (default 1 hour, max 24 hours). Implement server-side session management with DynamoDB TTL for automatic cleanup. Use Lambda functions to enforce session termination policies based on time or conditions.'
    },
    'ac-14': {
        'title': 'Permitted Actions Without Identification',
        'description': 'Identify and control actions permitted without authentication',
        'services': ['API Gateway', 'Lambda', 'S3', 'CloudFront'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document all unauthenticated endpoints in API Gateway. Use S3 bucket policies to explicitly define public access. Implement least privilege for unauthenticated Lambda functions. Review CloudFront distributions for public content. Use AWS Config to detect unintended public access.'
    },
    'ac-18': {
        'title': 'Wireless Access',
        'description': 'Establish wireless access restrictions and controls',
        'services': ['VPC', 'Direct Connect', 'Client VPN'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'For AWS Workspaces: Configure wireless network policies. For remote access: Use AWS Client VPN with certificate-based authentication. Avoid wireless for production AWS access - use Direct Connect or VPN over wired connections. Document wireless usage policies for accessing AWS Console.'
    },
    'ac-19': {
        'title': 'Access Control for Mobile Devices',
        'description': 'Establish mobile device access restrictions',
        'services': ['WorkSpaces', 'AppStream', 'IAM', 'Device Farm'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use AWS WorkSpaces for secure mobile access to corporate resources. Implement IAM policies that restrict access based on device compliance. Use AppStream 2.0 for application streaming to mobile devices. Require MFA for mobile device access to AWS Console.'
    },
    'ac-20': {
        'title': 'Use of External Systems',
        'description': 'Control use of external information systems',
        'services': ['IAM', 'Organizations', 'CloudTrail'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use IAM policies to restrict access from external systems. Implement SCPs in AWS Organizations to control cross-account access. Monitor external access with CloudTrail. Use VPC endpoints to keep traffic within AWS network. Document approved external systems and access methods.'
    },
    'ac-21': {
        'title': 'Information Sharing',
        'description': 'Control information sharing with external parties',
        'services': ['S3', 'Transfer Family', 'DataSync', 'IAM'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use S3 bucket policies with time-limited presigned URLs for external sharing. Implement AWS Transfer Family for secure file transfers. Use IAM roles for cross-account access with external AWS accounts. Enable S3 Object Lock for immutable sharing. Monitor sharing with CloudTrail and S3 Access Logs.'
    },
    'ac-22': {
        'title': 'Publicly Accessible Content',
        'description': 'Control publicly accessible information',
        'services': ['S3', 'CloudFront', 'API Gateway', 'Config'],
        'config_rules': ['s3-bucket-public-read-prohibited', 's3-bucket-public-write-prohibited'],
        'security_hub_controls': ['S3.1', 'S3.2'],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use S3 Block Public Access at account and bucket level. Implement approval workflow for making content public. Use CloudFront with OAI for controlled public access. Enable AWS Config rules to detect public S3 buckets. Review public content regularly with Access Analyzer.'
    },
    
    # Awareness and Training (AT)
    'at-1': {
        'title': 'Security Awareness and Training Policy',
        'description': 'Establish security awareness and training policies',
        'services': ['IAM', 'CloudWatch', 'Security Hub'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document security training requirements in your security policy. Use IAM to track user roles and required training. Maintain training records in a secure S3 bucket. Use CloudWatch Events to trigger training reminders. Integrate with your LMS or use AWS Partner solutions for training delivery.'
    },
    'at-2': {
        'title': 'Security Awareness Training',
        'description': 'Provide security awareness training to all users',
        'services': ['WorkDocs', 'Chime', 'S3'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Deliver training materials via S3-hosted content or WorkDocs. Use Chime for virtual training sessions. Track completion with Lambda functions and DynamoDB. Cover AWS-specific topics: IAM best practices, MFA usage, phishing awareness, data classification, incident reporting.'
    },
    'at-3': {
        'title': 'Role-Based Security Training',
        'description': 'Provide role-based security training',
        'services': ['IAM', 'Organizations', 'CloudWatch'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Map IAM roles to training requirements. Provide specialized training for: AWS administrators (IAM, security services), developers (secure coding, secrets management), security team (GuardDuty, Security Hub, incident response). Track role-based training completion in DynamoDB.'
    },
    'at-4': {
        'title': 'Security Training Records',
        'description': 'Document and monitor security training',
        'services': ['S3', 'DynamoDB', 'Lambda', 'CloudWatch'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Store training records in S3 with encryption. Use DynamoDB to track completion dates and expiration. Create CloudWatch dashboards for training compliance. Set up Lambda functions to send reminders for expiring training. Generate compliance reports with Athena queries.'
    },
    
    # Audit and Accountability (AU)
    'au-5': {
        'title': 'Response to Audit Processing Failures',
        'description': 'Alert on audit processing failures',
        'services': ['CloudWatch', 'SNS', 'Lambda', 'EventBridge'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Create CloudWatch alarms for CloudTrail delivery failures, S3 bucket access errors, and log storage capacity. Use SNS to alert security team. Implement Lambda functions to take corrective action (e.g., increase storage, fix permissions). Monitor CloudWatch Logs delivery with EventBridge rules.'
    },
    'au-7': {
        'title': 'Audit Reduction and Report Generation',
        'description': 'Provide audit analysis and reporting capabilities',
        'services': ['Athena', 'QuickSight', 'CloudWatch Insights', 'OpenSearch'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use Athena to query CloudTrail logs in S3. Create QuickSight dashboards for audit visualization. Use CloudWatch Logs Insights for real-time analysis. Deploy OpenSearch for advanced log analytics. Create saved queries for common audit reports (failed logins, privilege escalation, data access).'
    },
    'au-8': {
        'title': 'Time Stamps',
        'description': 'Use synchronized time stamps for audit records',
        'services': ['CloudTrail', 'CloudWatch', 'NTP'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'AWS services automatically use UTC timestamps. For EC2 instances, configure NTP using Amazon Time Sync Service (169.254.169.123). Verify time synchronization with Systems Manager. All CloudTrail events include precise timestamps. Use CloudWatch Logs timestamp for correlation across services.'
    },
    
    # Assessment, Authorization, and Monitoring (CA)
    'ca-1': {
        'title': 'Security Assessment and Authorization Policies',
        'description': 'Establish assessment and authorization policies',
        'services': ['Audit Manager', 'Security Hub', 'Config'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document assessment procedures in your security policy. Use AWS Audit Manager to automate evidence collection. Define authorization boundaries for AWS accounts and workloads. Implement continuous monitoring with Security Hub and Config. Document system authorization decisions in S3 with versioning.'
    },
    'ca-3': {
        'title': 'System Interconnections',
        'description': 'Authorize and monitor system interconnections',
        'services': ['VPC', 'Transit Gateway', 'PrivateLink', 'CloudTrail'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document all VPC peering connections, Transit Gateway attachments, and PrivateLink endpoints. Use VPC Flow Logs to monitor interconnection traffic. Implement security groups and NACLs at interconnection points. Review and approve new interconnections through change management. Monitor with CloudTrail and Config.'
    },
    'ca-5': {
        'title': 'Plan of Action and Milestones',
        'description': 'Develop and maintain POA&M for security weaknesses',
        'services': ['Security Hub', 'Systems Manager', 'Jira integration'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use Security Hub findings as input for POA&M. Track remediation in Systems Manager OpsCenter or integrate with Jira. Document milestones and responsible parties. Use Lambda to auto-create tickets for critical findings. Generate POA&M reports with Athena queries on Security Hub data.'
    },
    'ca-6': {
        'title': 'Security Authorization',
        'description': 'Assign senior official to authorize system operation',
        'services': ['Audit Manager', 'S3', 'IAM'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document authorization process and approving officials. Use AWS Audit Manager to collect authorization evidence. Store authorization packages in S3 with encryption and versioning. Implement IAM policies to restrict system access until authorized. Set authorization expiration dates with CloudWatch Events reminders.'
    },
    'ca-7': {
        'title': 'Continuous Monitoring',
        'description': 'Develop and implement continuous monitoring strategy',
        'services': ['Security Hub', 'Config', 'GuardDuty', 'CloudWatch', 'Systems Manager'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Enable Security Hub for centralized monitoring. Use Config for configuration compliance. Enable GuardDuty for threat detection. Create CloudWatch dashboards for security metrics. Use Systems Manager for patch compliance. Implement automated remediation with Lambda. Generate monthly monitoring reports.'
    },
    
    # Configuration Management (CM)
    'cm-5': {
        'title': 'Access Restrictions for Change',
        'description': 'Define and enforce access restrictions for changes',
        'services': ['IAM', 'Organizations', 'CloudFormation', 'CodePipeline'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use IAM policies to restrict who can modify infrastructure. Implement SCPs in Organizations to prevent unauthorized changes. Require all changes through CloudFormation or Terraform. Use CodePipeline with approval stages. Enable MFA delete on S3 buckets. Monitor changes with CloudTrail and Config.'
    },
    
    # Contingency Planning (CP)
    'cp-8': {
        'title': 'Telecommunications Services',
        'description': 'Establish alternate telecommunications services',
        'services': ['Direct Connect', 'VPN', 'Route 53'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Implement redundant connectivity: primary Direct Connect with VPN backup. Use multiple Direct Connect locations for diversity. Configure Route 53 health checks for automatic failover. Document telecommunications providers and SLAs. Test failover procedures quarterly. Consider multiple ISPs for VPN connections.'
    },
    
    # Identification and Authentication (IA)
    'ia-7': {
        'title': 'Cryptographic Module Authentication',
        'description': 'Implement authentication mechanisms for cryptographic modules',
        'services': ['KMS', 'CloudHSM', 'IAM'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use AWS KMS with IAM policies for key access control. For FIPS 140-2 Level 3, use CloudHSM with client authentication. Implement key policies requiring multiple approvers for sensitive operations. Use CloudTrail to audit all cryptographic operations. Rotate CloudHSM credentials regularly.'
    },
    
    # Incident Response (IR)
    'ir-1': {
        'title': 'Incident Response Policy and Procedures',
        'description': 'Establish incident response policies',
        'services': ['Security Hub', 'GuardDuty', 'Systems Manager'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document incident response procedures for AWS environments. Define incident categories and severity levels. Establish response team roles and contact information. Use Systems Manager for incident response automation. Store runbooks in S3 or Systems Manager Documents. Integrate with PagerDuty or similar for alerting.'
    },
    'ir-2': {
        'title': 'Incident Response Training',
        'description': 'Provide incident response training',
        'services': ['GameDay', 'CloudFormation', 'Lambda'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Conduct AWS-specific incident response training. Use AWS GameDay for hands-on practice. Create test environments with CloudFormation for incident simulation. Train on: GuardDuty findings, Security Hub alerts, CloudTrail analysis, EC2 forensics, S3 data breach response. Document training completion in DynamoDB.'
    },
    'ir-3': {
        'title': 'Incident Response Testing',
        'description': 'Test incident response capability',
        'services': ['CloudFormation', 'Lambda', 'EventBridge'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Conduct tabletop exercises quarterly. Perform technical tests in isolated AWS accounts. Use CloudFormation to create test scenarios. Simulate incidents: compromised IAM credentials, data exfiltration, ransomware, DDoS. Use Lambda to inject test events. Document test results and lessons learned in S3.'
    },
    'ir-7': {
        'title': 'Incident Response Assistance',
        'description': 'Provide incident response support resources',
        'services': ['Support', 'Security Hub', 'Systems Manager'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Maintain AWS Enterprise Support for 24/7 incident assistance. Document AWS Support contact procedures. Create Systems Manager runbooks for common incidents. Establish relationships with AWS Security team. Use AWS Professional Services for complex incidents. Document internal and external support contacts.'
    },
    'ir-8': {
        'title': 'Incident Response Plan',
        'description': 'Develop and implement incident response plan',
        'services': ['Systems Manager', 'Lambda', 'Step Functions'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Create comprehensive IR plan covering AWS-specific scenarios. Use Systems Manager Automation for response playbooks. Implement Step Functions for complex response workflows. Define escalation procedures and communication plans. Include procedures for: account compromise, data breach, service disruption, insider threat. Review and update plan annually.'
    },
    
    # Maintenance (MA)
    'ma-1': {
        'title': 'System Maintenance Policy and Procedures',
        'description': 'Establish maintenance policies',
        'services': ['Systems Manager', 'CloudWatch', 'Config'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document maintenance procedures for AWS resources. Use Systems Manager Maintenance Windows for scheduled maintenance. Define approval requirements for maintenance activities. Track maintenance with Config and CloudTrail. Implement change management for infrastructure updates. Document emergency maintenance procedures.'
    },
    
    # Media Protection (MP)
    'mp-1': {
        'title': 'Media Protection Policy and Procedures',
        'description': 'Establish media protection policies',
        'services': ['S3', 'EBS', 'Backup', 'Storage Gateway'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document policies for protecting data at rest. Require encryption for all storage: S3, EBS, RDS, EFS. Define data classification and handling procedures. Use S3 Object Lock for immutable storage. Implement backup retention policies with AWS Backup. Document media sanitization procedures (delete with verification).'
    },
    'mp-2': {
        'title': 'Media Access',
        'description': 'Restrict access to digital and non-digital media',
        'services': ['S3', 'IAM', 'KMS', 'Macie'],
        'config_rules': ['s3-bucket-public-read-prohibited', 's3-bucket-public-write-prohibited'],
        'security_hub_controls': ['S3.1', 'S3.2'],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use IAM policies to control S3 bucket access. Enable S3 Block Public Access. Encrypt data with KMS and control key access. Use Macie to discover sensitive data. Implement least privilege for EBS volume access. Monitor access with CloudTrail and S3 Access Logs. Use VPC endpoints to keep traffic private.'
    },
    'mp-3': {
        'title': 'Media Marking',
        'description': 'Mark media indicating distribution limitations',
        'services': ['S3', 'Tags', 'Macie'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use S3 object tags to mark data classification (Public, Internal, Confidential, Restricted). Apply tags to EBS volumes and snapshots. Use Macie to auto-classify and tag sensitive data. Implement tag-based IAM policies for access control. Create CloudWatch dashboards showing data classification distribution. Enforce tagging with Config rules.'
    },
    'mp-4': {
        'title': 'Media Storage',
        'description': 'Physically control and securely store media',
        'services': ['S3', 'Glacier', 'Backup', 'Storage Gateway'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Store backups in S3 with encryption and versioning. Use S3 Glacier for long-term archival. Enable S3 Object Lock for compliance retention. Use AWS Backup for centralized backup management. Implement cross-region replication for geographic diversity. For physical media (if any), document storage in secure AWS data centers.'
    },
    'mp-5': {
        'title': 'Media Transport',
        'description': 'Protect and control media during transport',
        'services': ['Snowball', 'DataSync', 'Transfer Family', 'S3'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Use AWS Snowball for large data transfers with built-in encryption. Use DataSync for secure online transfers. Implement Transfer Family with encryption for file transfers. Use S3 Transfer Acceleration with TLS. For physical media transport, use AWS Import/Export with encryption. Document chain of custody procedures.'
    },
    'mp-6': {
        'title': 'Media Sanitization',
        'description': 'Sanitize media before disposal or reuse',
        'services': ['S3', 'EBS', 'KMS'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Delete S3 objects and verify deletion. Delete EBS volumes and snapshots. For encrypted data, delete KMS keys to make data unrecoverable. Use S3 Object Lock delete markers for audit trail. AWS handles physical media destruction per NIST 800-88. Document sanitization procedures and maintain deletion logs in CloudTrail.'
    },
    
    # Planning (PL)
    'pl-2': {
        'title': 'System Security Plan',
        'description': 'Develop and maintain system security plan',
        'services': ['Audit Manager', 'S3', 'Systems Manager'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document security plan for each AWS workload/account. Use AWS Audit Manager templates as starting point. Include: system architecture, security controls, data flows, interconnections, responsible parties. Store plans in S3 with versioning. Use Systems Manager Parameter Store for configuration details. Review and update plans annually or after significant changes.'
    },
    'pl-4': {
        'title': 'Rules of Behavior',
        'description': 'Establish rules of behavior for system users',
        'services': ['IAM', 'Cognito', 'S3'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Document acceptable use policies for AWS resources. Present rules during user onboarding. Use Cognito pre-authentication triggers to require acceptance. Store signed acknowledgments in S3. Include rules for: password management, MFA usage, data handling, incident reporting, remote access. Review and update rules annually.'
    },
    'pl-8': {
        'title': 'Information Security Architecture',
        'description': 'Develop information security architecture',
        'services': ['Organizations', 'Control Tower', 'CloudFormation'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Design multi-account architecture using AWS Organizations. Implement landing zone with Control Tower. Define security zones: production, development, DMZ. Use CloudFormation for infrastructure as code. Document network architecture with VPCs, subnets, security groups. Implement defense in depth: WAF, Shield, GuardDuty, Security Hub. Review architecture quarterly.'
    },
    'pl-10': {
        'title': 'Baseline Selection',
        'description': 'Select security control baseline',
        'services': ['Security Hub', 'Config', 'Audit Manager'],
        'config_rules': [],
        'security_hub_controls': [],
        'control_tower_ids': [],
        'frameworks': ['NIST-800-53'],
        'implementation': 'Select appropriate NIST 800-53 baseline (Low, Moderate, High). Enable Security Hub standards (AWS Foundational, CIS, PCI-DSS). Use Config conformance packs for baseline enforcement. Document baseline selection rationale. Implement baseline controls with CloudFormation. Use Audit Manager to track baseline compliance.'
    },
}


def load_existing_mcp_data():
    """Load existing MCP data."""
    mcp_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    if mcp_file.exists():
        with open(mcp_file, 'r') as f:
            data = json.load(f)
            return data.get('controls', {})
    return {}


def save_mcp_data(controls_data):
    """Save MCP data to JSON file."""
    mcp_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    
    output = {
        'metadata': {
            'source': 'AWS best practices and service documentation',
            'description': 'AWS implementation guides for NIST 800-53 controls',
            'total_controls': len(controls_data)
        },
        'controls': controls_data
    }
    
    with open(mcp_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved {len(controls_data)} controls to {mcp_file}")


def main():
    """Main function to add customer control guides."""
    print("Loading NIST 800-53 controls...")
    parser = NIST80053Parser()
    controls = parser.get_moderate_baseline_controls()
    
    # Load existing data
    mcp_data = load_existing_mcp_data()
    print(f"Loaded {len(mcp_data)} existing control guides")
    
    # Add new customer control guides
    added_count = 0
    for control_id, guide_data in CUSTOMER_CONTROL_GUIDES.items():
        if control_id not in mcp_data:
            # Format the guide data to match MCP structure
            mcp_data[control_id] = [{
                'control_id': f'AWS-CG-{control_id.upper()}',
                'title': guide_data['title'],
                'description': guide_data['description'],
                'services': guide_data['services'],
                'config_rules': guide_data['config_rules'],
                'security_hub_controls': guide_data['security_hub_controls'],
                'control_tower_ids': guide_data['control_tower_ids'],
                'frameworks': guide_data['frameworks'],
                'implementation_guidance': guide_data.get('implementation', '')
            }]
            added_count += 1
            print(f"Added guide for {control_id.upper()}: {guide_data['title']}")
    
    if added_count > 0:
        save_mcp_data(mcp_data)
        print(f"\n✓ Added {added_count} new customer control guides")
    else:
        print("\nNo new guides to add - all controls already have guides")
    
    # Show remaining controls without guides
    remaining = []
    for control in controls:
        control_id = control.id.lower()
        resp = get_aws_responsibility(control_id)
        if resp == 'customer' and control_id not in mcp_data:
            remaining.append(control_id)
    
    if remaining:
        print(f"\n{len(remaining)} customer controls still need guides:")
        for cid in sorted(remaining)[:10]:
            print(f"  {cid}")
        if len(remaining) > 10:
            print(f"  ... and {len(remaining) - 10} more")


if __name__ == '__main__':
    main()

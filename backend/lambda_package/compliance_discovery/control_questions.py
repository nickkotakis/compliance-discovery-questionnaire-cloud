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
            'type': 'shared_responsibility',
            'question': 'Does your physical security policy acknowledge AWS shared responsibility model (AWS secures data centers, you secure access to AWS services)? Have you reviewed AWS compliance reports in AWS Artifact?',
        },
        {
            'type': 'on_premises_controls',
            'question': 'For any on-premises infrastructure (Direct Connect, hybrid cloud), what physical security controls are in place (access control, surveillance, environmental monitoring)?',
        },
        {
            'type': 'policy_review',
            'question': 'When was your physical security policy last reviewed and updated? Does it address remote work and endpoint security for AWS access?',
        },
    ],
    'pe-4': [
        {
            'type': 'transmission_protection',
            'question': 'For Direct Connect or hybrid connections to AWS, how are transmission lines physically protected (locked cabinets, conduits, restricted access areas)?',
        },
        {
            'type': 'on_premises_network',
            'question': 'For on-premises infrastructure, are network cables in locked wiring closets? Are unused network ports disabled or secured?',
        },
        {
            'type': 'aws_acknowledgment',
            'question': 'Do you acknowledge that AWS is responsible for physical transmission line security within their data centers? Have you documented this in your system security plan?',
        },
    ],
    'pe-17': [
        {
            'type': 'remote_work_policy',
            'question': 'Do you have a documented remote work policy that specifies security requirements for accessing AWS resources? Does it mandate VPN, MFA, and endpoint security controls?',
        },
        {
            'type': 'remote_access_controls',
            'question': 'What technical controls enforce secure remote access to AWS (AWS Client VPN, Systems Manager Session Manager, third-party VPN with MFA)? How is compliance monitored?',
        },
        {
            'type': 'endpoint_security',
            'question': 'What endpoint security requirements exist for remote devices (antivirus, disk encryption, OS patching, device management)? How do you verify compliance before allowing AWS access?',
        },
    ],
    
    # Awareness and Training
    'at-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have a documented security awareness and training policy? Does it specify training frequency, topics, and target audiences (all users, privileged users, developers)?',
        },
        {
            'type': 'aws_specific_training',
            'question': 'Does your training policy address AWS-specific security topics (IAM best practices, S3 bucket security, CloudTrail logging, incident response in AWS)?',
        },
        {
            'type': 'policy_review',
            'question': 'When was your security awareness and training policy last reviewed and updated? Does it reflect current AWS services and threats?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AT-1 compliance? Provide: Training policy document with approval signatures, policy review records, training curriculum documentation. Where are these artifacts stored?',
        },
    ],
    'at-2': [
        {
            'type': 'training_program',
            'question': 'What security awareness training do all AWS users receive? Does it cover phishing, password security, MFA, data classification, and acceptable use?',
        },
        {
            'type': 'aws_security_topics',
            'question': 'Does your training include AWS-specific security awareness (recognizing suspicious CloudTrail events, understanding IAM permissions, securing S3 buckets, reporting security findings)?',
        },
        {
            'type': 'training_frequency',
            'question': 'How often is security awareness training provided (onboarding, annually, after security incidents)? What is the completion rate? How do you track and enforce completion?',
        },
        {
            'type': 'training_delivery',
            'question': 'How is training delivered (online modules, in-person sessions, videos, documentation)? Is it tailored for different roles (developers, administrators, end users)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AT-2 compliance? Provide: Training completion records, training materials/curriculum, attendance logs, quiz/assessment results, training platform screenshots. Where are these artifacts stored?',
        },
    ],
    'at-3': [
        {
            'type': 'role_based_training',
            'question': 'What role-based security training is provided for AWS administrators, developers, and security personnel? Does it go beyond basic awareness?',
        },
        {
            'type': 'aws_technical_training',
            'question': 'What AWS-specific technical training do privileged users receive (AWS Security Specialty certification, Well-Architected Framework, security best practices, incident response procedures)?',
        },
        {
            'type': 'training_requirements',
            'question': 'What are the training requirements for different roles (initial training, annual refresher, training after role changes)? Are AWS certifications required or encouraged?',
        },
        {
            'type': 'training_effectiveness',
            'question': 'How do you measure training effectiveness (assessments, hands-on labs, simulated incidents, security metrics improvement)? What is the pass rate?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AT-3 compliance? Provide: Role-based training curriculum, completion records by role, certification records, assessment results, training platform reports. Where are these artifacts stored?',
        },
    ],
    'at-4': [
        {
            'type': 'incident_recognition',
            'question': 'What training do users receive on recognizing security incidents in AWS (unusual GuardDuty findings, suspicious CloudTrail events, unauthorized access attempts, data exfiltration)?',
        },
        {
            'type': 'reporting_procedures',
            'question': 'Do users know how to report security incidents? Is there a clear escalation path (security team email, ticketing system, incident response hotline)?',
        },
        {
            'type': 'aws_incident_scenarios',
            'question': 'Does training include AWS-specific incident scenarios (compromised IAM credentials, exposed S3 bucket, EC2 instance compromise, DDoS attack)? Are there tabletop exercises?',
        },
        {
            'type': 'training_updates',
            'question': 'How often is incident recognition training updated to reflect new threats and AWS security findings? Are users notified of new attack patterns?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AT-4 compliance? Provide: Incident recognition training materials, reporting procedure documentation, training completion records, tabletop exercise reports. Where are these artifacts stored?',
        },
    ],
    
    # Access Control
    'ac-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have a documented access control policy for AWS that covers IAM users, roles, and the principle of least privilege? When was it last reviewed?',
        },
        {
            'type': 'policy_enforcement',
            'question': 'How is your access control policy enforced in AWS (SCPs, permission boundaries, IAM policies)? Are there automated checks for policy violations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AC-1 compliance in AWS? Provide: Configuration screenshots from AWS Identity and Access Management, AWS Organizations; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ac-2': [
        {
            'type': 'account_lifecycle',
            'question': 'What is your process for provisioning and deprovisioning IAM users and roles? Who approves new access, and how quickly are terminated employees removed?',
        },
        {
            'type': 'account_review',
            'question': 'How often do you review IAM users and roles for appropriateness? Are you using IAM Access Analyzer or Access Advisor to identify unused permissions?',
        },
        {
            'type': 'privileged_accounts',
            'question': 'How are privileged AWS accounts managed (root account, admin roles)? Is MFA enforced, and are privileged actions logged and monitored?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AC-2 compliance in AWS? Provide: AWS Config compliance reports for MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, IAM_GROUP_HAS_USERS_CHECK, IAM_POLICY_IN_USE (and 1 more); Security Hub findings for IAM.5, IAM.18, IAM.19 (and 3 more); Control Tower compliance status for AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, SH.IAM.5 (and 5 more); Configuration screenshots from AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ac-3': [
        {
            'type': 'authorization_enforcement',
            'question': 'How do you enforce least privilege in AWS? Are you using IAM policies, resource policies, SCPs, and permission boundaries together?',
        },
        {
            'type': 'access_validation',
            'question': 'How do you validate that IAM policies grant only necessary permissions? Are you using IAM Access Analyzer policy validation or conducting regular access reviews?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AC-3 compliance in AWS? Provide: AWS Config compliance reports for IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS, S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS, S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED (and 2 more); Security Hub findings for IAM.21, S3.1, S3.2 (and 3 more); Control Tower compliance status for SH.IAM.21, AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC (and 4 more); Configuration screenshots from AWS Identity and Access Management, Amazon Elastic Kubernetes Service, Amazon S3; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ac-6': [
        {
            'type': 'least_privilege_implementation',
            'question': 'How do you implement least privilege for IAM roles and users? Do you start with minimal permissions and add as needed, or remove from broad permissions?',
        },
        {
            'type': 'permission_analysis',
            'question': 'What tools do you use to identify excessive permissions (IAM Access Analyzer, Access Advisor, third-party tools)? How often are unused permissions removed?',
        },
        {
            'type': 'privileged_access',
            'question': 'How is privileged access controlled (break-glass procedures, time-limited elevated access, approval workflows)? Are privileged sessions monitored and recorded?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AC-6 compliance in AWS? Provide: AWS Config compliance reports for IAM_POLICY_IN_USE; Security Hub findings for IAM.18; Control Tower compliance status for CT.IAM.PR.1, CT.IAM.PR.5; Configuration screenshots from AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ac-17': [
        {
            'type': 'remote_access_methods',
            'question': 'What remote access methods are used to access AWS resources (AWS Client VPN, Systems Manager Session Manager, bastion hosts, Direct Connect)? Is MFA required?',
        },
        {
            'type': 'remote_access_monitoring',
            'question': 'How is remote access monitored and logged (CloudTrail, VPC Flow Logs, Session Manager logging)? Are alerts configured for suspicious remote access patterns?',
        },
        {
            'type': 'remote_access_restrictions',
            'question': 'What restrictions are in place for remote access (IP allowlists, time-based access, device compliance checks)? How are these enforced?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AC-17 compliance in AWS? Provide: AWS Config compliance reports for EKS_ENDPOINT_NO_PUBLIC_ACCESS, S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS, S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC (and 4 more); Security Hub findings for EKS.1, S3.1, S3.2 (and 3 more); Control Tower compliance status for AWS-GR_EKS_ENDPOINT_NO_PUBLIC_ACCESS, SH.EKS.1 (and 10 more); Configuration screenshots from Amazon Elastic Kubernetes Service, Amazon S3, Amazon SageMaker; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # Audit and Accountability
    'au-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have a documented audit policy that specifies what AWS events must be logged (CloudTrail, VPC Flow Logs, CloudWatch)? Does it define retention periods?',
        },
        {
            'type': 'log_protection',
            'question': 'How are AWS logs protected from unauthorized access and tampering? Are CloudTrail logs encrypted and stored in a separate account with restricted access?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AU-1 compliance in AWS? Provide: AWS Config compliance reports for CLOUDTRAIL_SECURITY_TRAIL_ENABLED, CW_LOGGROUP_RETENTION_PERIOD_CHECK; Security Hub findings for CloudTrail.3, CloudWatch.16; Control Tower compliance status for CONFIG.CLOUDTRAIL.DT.6, CONFIG.LOGS.DT.2; Configuration screenshots from AWS CloudTrail, AWS Organizations, Amazon CloudWatch Logs (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'au-2': [
        {
            'type': 'logging_coverage',
            'question': 'Is CloudTrail enabled in all regions and accounts? Are you logging management events, data events (S3, Lambda), and Insights events?',
        },
        {
            'type': 'additional_logging',
            'question': 'What additional logging is enabled (VPC Flow Logs, CloudWatch Logs, application logs, database audit logs)? How is this centralized?',
        },
        {
            'type': 'log_analysis',
            'question': 'How are logs analyzed for security events? Are you using CloudWatch Insights, Athena, or a SIEM tool to detect anomalies?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AU-2 compliance in AWS? Provide: AWS Config compliance reports for MULTI_REGION_CLOUD_TRAIL_ENABLED, CLOUDTRAIL_SECURITY_TRAIL_ENABLED, CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED (and 2 more); Security Hub findings for CloudTrail.1, CloudTrail.3, CloudTrail.4 (and 2 more); Control Tower compliance status for SH.CloudTrail.1, CONFIG.CLOUDTRAIL.DT.6 (and 5 more); Configuration screenshots from AWS CloudTrail; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'au-3': [
        {
            'type': 'audit_content',
            'question': 'What information is captured in CloudTrail logs (who, what, when, where, source IP, user agent)? Are you logging request and response elements for critical APIs?',
        },
        {
            'type': 'log_enrichment',
            'question': 'Are logs enriched with additional context (resource tags, account metadata, threat intelligence)? How is this information used for investigations?',
        },
        {
            'type': 'log_completeness',
            'question': 'How do you ensure audit logs are complete and not missing events? Are CloudTrail log file validation and digest files enabled?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AU-3 compliance in AWS? Provide: AWS Config compliance reports for MULTI_REGION_CLOUD_TRAIL_ENABLED, CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED, CLOUDTRAIL_ALL_READ_S3_DATA_EVENT_CHECK; Security Hub findings for CloudTrail.1, CloudTrail.4; Control Tower compliance status for SH.CloudTrail.1, CT.CLOUDTRAIL.PR.2 (and 2 more); Configuration screenshots from AWS CloudTrail; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'au-6': [
        {
            'type': 'log_review_process',
            'question': 'How often are AWS logs reviewed for security events (real-time, daily, weekly)? Who is responsible for log review and analysis?',
        },
        {
            'type': 'automated_analysis',
            'question': 'What automated tools analyze logs (GuardDuty, Security Hub, CloudWatch anomaly detection, SIEM)? What types of events trigger alerts?',
        },
        {
            'type': 'investigation_process',
            'question': 'When suspicious activity is detected in logs, what is the investigation process? Are CloudTrail Insights or Athena queries used for deep analysis?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AU-6 compliance in AWS? Provide: AWS Config compliance reports for CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK, CW_LOGGROUP_RETENTION_PERIOD_CHECK, SECURITYHUB_ENABLED; Security Hub findings for CloudWatch.17, CloudWatch.16; Control Tower compliance status for CONFIG.CLOUDWATCH.DT.1, CONFIG.LOGS.DT.2 (and 1 more); Configuration screenshots from AWS Security Hub, Amazon CloudWatch, Amazon CloudWatch Logs; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'au-9': [
        {
            'type': 'log_access_control',
            'question': 'Who has access to CloudTrail logs and other audit data? Are logs stored in a separate security/logging account with restricted access?',
        },
        {
            'type': 'log_encryption',
            'question': 'Are CloudTrail logs encrypted at rest with KMS? Are S3 bucket policies configured to prevent unauthorized access and deletion?',
        },
        {
            'type': 'log_integrity',
            'question': 'How do you protect log integrity (CloudTrail log file validation, S3 Object Lock, MFA Delete)? Can logs be tampered with or deleted?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates AU-9 compliance in AWS? Provide: AWS Config compliance reports for S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED; Security Hub findings for CloudTrail.6, S3.8; Control Tower compliance status for AWS-GR_AUDIT_BUCKET_RETENTION_POLICY, AWS-GR_AUDIT_BUCKET_POLICY_CHANGES_PROHIBITED (and 2 more); Configuration screenshots from AWS CloudTrail, Amazon S3; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # Configuration Management
    'cm-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have a configuration management policy that requires Infrastructure as Code (CloudFormation, Terraform, CDK) for all AWS resources?',
        },
        {
            'type': 'change_control',
            'question': 'What is your change control process for AWS infrastructure? Are all changes peer-reviewed, tested in non-prod, and tracked in version control?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CM-1 compliance in AWS? Provide: AWS Config compliance reports for CLOUDFORMATION_STACK_NOTIFICATION_CHECK; Security Hub findings for CloudFormation.1; Control Tower compliance status for AWS-GR_CONFIG_ENABLED, CONFIG.CLOUDFORMATION.DT.1; Configuration screenshots from AWS CloudFormation, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cm-2': [
        {
            'type': 'baseline_configs',
            'question': 'Are baseline configurations documented for AWS resources (EC2 AMIs, RDS parameter groups, security group templates)? How are they maintained and updated?',
        },
        {
            'type': 'drift_detection',
            'question': 'How do you detect and remediate configuration drift? Are you using AWS Config rules, CloudFormation drift detection, or third-party tools?',
        },
        {
            'type': 'compliance_monitoring',
            'question': 'What AWS Config rules or custom policies enforce your baseline configurations? How are non-compliant resources identified and remediated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CM-2 compliance in AWS? Provide: AWS Config compliance reports for EBS_IN_BACKUP_PLAN, EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN; Security Hub findings for EC2.28; Control Tower compliance status for AWS-GR_CONFIG_CHANGE_PROHIBITED, AWS-GR_CONFIG_RULE_CHANGE_PROHIBITED (and 2 more); Configuration screenshots from AWS Config, Amazon Elastic Block Store; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cm-3': [
        {
            'type': 'change_approval',
            'question': 'What is the approval process for AWS infrastructure changes? Who must approve changes to production environments?',
        },
        {
            'type': 'change_testing',
            'question': 'How are infrastructure changes tested before production deployment (dev/staging environments, automated testing, rollback procedures)?',
        },
        {
            'type': 'change_tracking',
            'question': 'How are infrastructure changes tracked and documented (Git commits, change tickets, CloudTrail logs)? Can you trace who made what change and when?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CM-3 compliance in AWS? Provide: AWS Config compliance reports for CLOUDFORMATION_STACK_NOTIFICATION_CHECK; Security Hub findings for CloudFormation.1; Control Tower compliance status for AWS-GR_CONFIG_CHANGE_PROHIBITED, CONFIG.CLOUDFORMATION.DT.1 (and 1 more); Configuration screenshots from AWS CloudFormation, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cm-7': [
        {
            'type': 'service_minimization',
            'question': 'What process ensures only necessary AWS services are enabled? Are unused services and features disabled (unused regions, unnecessary APIs)?',
        },
        {
            'type': 'port_protocol_restriction',
            'question': 'How are unnecessary ports and protocols restricted (security groups with minimal rules, NACLs, AWS Network Firewall)? Are default-deny rules enforced?',
        },
        {
            'type': 'function_restriction',
            'question': 'Are unnecessary functions disabled on EC2 instances and containers (unused services, unnecessary software packages)? How is this enforced in AMIs and container images?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CM-7 compliance in AWS? Provide: AWS Config compliance reports for SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED, INCOMING_SSH_DISABLED, EC2_SECURITY_GROUP_ATTACHED_TO_ENI (and 1 more); Security Hub findings for EC2.15, EC2.13, EC2.22; Control Tower compliance status for AWS-GR_SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED, SH.EC2.15 (and 3 more); Configuration screenshots from Amazon EC2, Amazon VPC Lattice; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cm-8': [
        {
            'type': 'asset_inventory',
            'question': 'How do you maintain an inventory of AWS resources (AWS Config, Systems Manager Inventory, third-party CMDB)? Is the inventory automatically updated?',
        },
        {
            'type': 'inventory_accuracy',
            'question': 'How often is the asset inventory validated for accuracy? Can you identify all EC2 instances, Lambda functions, S3 buckets, and other resources?',
        },
        {
            'type': 'inventory_metadata',
            'question': 'What metadata is tracked for each asset (owner, purpose, environment, data classification, compliance requirements)? Are resources tagged consistently?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CM-8 compliance in AWS? Provide: Control Tower compliance status for CONFIG.APPCONFIG.DT.1, AWS-GR_CONFIG_CHANGE_PROHIBITED; Configuration screenshots from AWS AppConfig, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # Identification and Authentication
    'ia-1': [
        {
            'type': 'policy_requirements',
            'question': 'What authentication requirements are documented in your AWS access policy (MFA for console, federated access via SSO, no long-term access keys)? When was it last updated?',
        },
        {
            'type': 'federation_implementation',
            'question': 'Are you using AWS IAM Identity Center or a third-party IdP (Okta, Azure AD) for federated access? What percentage of users authenticate via federation vs. direct IAM users?',
        },
        {
            'type': 'policy_enforcement',
            'question': 'How do you enforce authentication requirements (SCPs requiring MFA, automated detection of IAM users without MFA, alerts for access key age)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates IA-1 compliance in AWS? Provide: AWS Config compliance reports for IAM_PASSWORD_POLICY; Security Hub findings for IAM.7, IAM.8, IAM.9 (and 2 more); Control Tower compliance status for SH.IAM.7, SH.IAM.8; Configuration screenshots from AWS IAM Identity Center, AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ia-2': [
        {
            'type': 'mfa_enforcement',
            'question': 'What percentage of IAM users have MFA enabled? Is MFA required for root account and all privileged roles? How do you monitor and enforce this?',
        },
        {
            'type': 'authentication_mechanisms',
            'question': 'What authentication mechanisms are used (hardware MFA tokens, virtual MFA apps, FIDO2 security keys)? Are programmatic access keys rotated regularly?',
        },
        {
            'type': 'password_requirements',
            'question': 'What are your IAM password requirements (minimum 14 characters, complexity, 90-day rotation)? Are these enforced via IAM password policy?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates IA-2 compliance in AWS? Provide: AWS Config compliance reports for MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, IAM_USER_MFA_ENABLED, ROOT_ACCOUNT_MFA_ENABLED; Security Hub findings for IAM.5, IAM.19, IAM.6; Control Tower compliance status for AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, SH.IAM.5 (and 3 more); Configuration screenshots from AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ia-5': [
        {
            'type': 'credential_management',
            'question': 'How are AWS credentials managed (IAM roles preferred over access keys, Secrets Manager for application credentials, no hardcoded credentials)?',
        },
        {
            'type': 'credential_rotation',
            'question': 'What is your credential rotation policy (access keys rotated every 90 days, passwords every 90 days, automatic rotation for Secrets Manager)?',
        },
        {
            'type': 'credential_protection',
            'question': 'How are credentials protected (Secrets Manager encryption, no credentials in code repositories, credential scanning in CI/CD)? What happens when credentials are exposed?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates IA-5 compliance in AWS? Provide: AWS Config compliance reports for SECRETSMANAGER_SECRET_UNUSED, MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, IAM_USER_MFA_ENABLED; Security Hub findings for SecretsManager.3, IAM.5, IAM.19; Control Tower compliance status for SH.SecretsManager.3, AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS (and 2 more); Configuration screenshots from AWS Identity and Access Management, AWS Secrets Manager; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # System and Communications Protection
    'sc-1': [
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
    ],
'sc-2': [
        {
            'type': 'separation_implementation',
            'question': 'How do you separate system and user functionality in AWS (separate VPCs for management vs application, separate AWS accounts, IAM role separation, resource tagging)?',
        },
        {
            'type': 'management_separation',
            'question': 'Are management functions separated from user functions (separate management VPC, Systems Manager for admin access, bastion hosts in separate subnets, PrivateLink for service access)?',
        },
        {
            'type': 'separation_enforcement',
            'question': 'How is separation enforced (security groups, NACLs, SCPs, IAM policies, VPC endpoints)? Can users access management functions?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-2 compliance? Provide: VPC architecture diagrams, security group configurations, IAM policy separation, account structure documentation. Where are these artifacts stored?',
        },
    ],
    'sc-4': [
        {
            'type': 'shared_resources',
            'question': 'What AWS resources are shared between workloads or tenants (shared VPCs, shared services, multi-tenant applications, shared databases)? Are they documented?',
        },
        {
            'type': 'information_protection',
            'question': 'How is information protected in shared resources (encryption, access controls, data isolation, separate schemas/tables, tenant ID filtering)?',
        },
        {
            'type': 'residual_information',
            'question': 'How do you prevent information leakage in shared resources (memory clearing, secure deletion, EBS volume encryption, RDS encryption, Lambda execution environment isolation)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-4 compliance? Provide: Shared resource inventory, data isolation mechanisms, encryption configurations, tenant separation documentation. Where are these artifacts stored?',
        },
    ],
    'sc-5': [
        {
            'type': 'ddos_protection',
            'question': 'What DDoS protection is in place for AWS resources (AWS Shield Standard/Advanced, CloudFront, Route 53, WAF rate limiting, Auto Scaling)?',
        },
        {
            'type': 'resource_limits',
            'question': 'How do you prevent resource exhaustion (service quotas, API rate limiting, Lambda concurrency limits, RDS connection limits, Auto Scaling policies)?',
        },
        {
            'type': 'ddos_response',
            'question': 'What is your DDoS response plan (Shield Response Team engagement, traffic analysis, mitigation strategies, communication plan)? Have you tested it?',
        },
        {
            'type': 'monitoring',
            'question': 'How do you monitor for DoS attacks (CloudWatch metrics, Shield Advanced detection, WAF blocked requests, GuardDuty findings, anomaly detection)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-5 compliance? Provide: Shield configurations, WAF rules, Auto Scaling policies, DDoS response plan, monitoring dashboards. Where are these artifacts stored?',
        },
    ],
    'sc-10': [
        {
            'type': 'session_termination',
            'question': 'How are inactive AWS sessions terminated (IAM session duration limits, SSO session timeout, console session timeout, API token expiration)?',
        },
        {
            'type': 'timeout_configuration',
            'question': 'What are your session timeout settings (console: 12 hours max, API tokens: 1 hour, SSO: configurable, database connections: timeout settings)?',
        },
        {
            'type': 'forced_disconnect',
            'question': 'Can sessions be forcibly disconnected (IAM session revocation, SSO session termination, Systems Manager session termination, emergency access revocation)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-10 compliance? Provide: IAM session duration policies, SSO timeout configurations, session termination logs, timeout enforcement documentation. Where are these artifacts stored?',
        },
    ],
    'sc-15': [
        {
            'type': 'collaborative_devices',
            'question': 'What collaborative computing devices/applications integrate with AWS (video conferencing, screen sharing, collaboration tools, remote access tools)? Are they approved?',
        },
        {
            'type': 'device_security',
            'question': 'How are collaborative devices secured when accessing AWS (endpoint security, MFA, VPN requirements, device compliance checks, approved applications list)?',
        },
        {
            'type': 'usage_restrictions',
            'question': 'What restrictions exist on collaborative device usage (no recording of sensitive data, no screen sharing of AWS console, approved tools only, data classification restrictions)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-15 compliance? Provide: Approved collaborative tools list, usage policy, endpoint security requirements, compliance monitoring reports. Where are these artifacts stored?',
        },
    ],
    'sc-17': [
        {
            'type': 'pki_certificates',
            'question': 'What PKI certificates are used in AWS (ACM certificates for load balancers, API Gateway custom domains, CloudFront distributions, IoT device certificates)?',
        },
        {
            'type': 'certificate_management',
            'question': 'How are certificates managed (AWS Certificate Manager for public certs, ACM Private CA for internal certs, automated renewal, expiration monitoring)?',
        },
        {
            'type': 'certificate_validation',
            'question': 'How are certificates validated (certificate transparency logs, OCSP/CRL checking, certificate pinning, automated validation)?',
        },
        {
            'type': 'certificate_revocation',
            'question': 'What is your certificate revocation process (ACM certificate deletion, Private CA revocation, CRL distribution, emergency revocation procedures)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-17 compliance? Provide: ACM certificate inventory, Private CA configuration, certificate renewal logs, revocation procedures. Where are these artifacts stored?',
        },
    ],
    'sc-18': [
        {
            'type': 'mobile_code',
            'question': 'What mobile code is used in AWS (JavaScript in web apps, Lambda functions, container images, browser extensions, mobile apps)?',
        },
        {
            'type': 'code_security',
            'question': 'How is mobile code secured (code signing, integrity verification, sandboxing, Lambda execution role restrictions, container image scanning)?',
        },
        {
            'type': 'code_approval',
            'question': 'What is your mobile code approval process (code review, security scanning, testing, deployment approval)? Are unapproved code deployments prevented?',
        },
        {
            'type': 'code_monitoring',
            'question': 'How is mobile code monitored (Lambda function monitoring, CloudWatch Logs, GuardDuty for malicious activity, runtime security)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-18 compliance? Provide: Mobile code inventory, code signing configurations, approval records, security scanning reports. Where are these artifacts stored?',
        },
    ],
    'sc-22': [
        {
            'type': 'dns_architecture',
            'question': 'What is your DNS architecture in AWS (Route 53 hosted zones, private hosted zones, DNS resolution in VPCs, hybrid DNS with on-premises)?',
        },
        {
            'type': 'dns_security',
            'question': 'How is DNS secured (DNSSEC for Route 53, DNS query logging, GuardDuty DNS protection, private hosted zones for internal resources)?',
        },
        {
            'type': 'dns_redundancy',
            'question': 'How is DNS availability ensured (Route 53 multi-region, health checks, failover routing, backup DNS servers)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-22 compliance? Provide: Route 53 hosted zone configurations, DNSSEC settings, DNS query logs, architecture diagrams. Where are these artifacts stored?',
        },
    ],
    'sc-23': [
        {
            'type': 'session_authenticity',
            'question': 'How do you ensure AWS session authenticity (TLS for all connections, certificate validation, MFA for console access, signed API requests)?',
        },
        {
            'type': 'session_protection',
            'question': 'How are sessions protected from hijacking (session tokens with short expiration, IP address binding, user agent validation, CloudTrail monitoring for anomalies)?',
        },
        {
            'type': 'session_monitoring',
            'question': 'How are suspicious sessions detected (GuardDuty for unusual API calls, CloudTrail analysis, impossible travel detection, concurrent session alerts)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-23 compliance? Provide: TLS configurations, session token policies, GuardDuty findings, session monitoring alerts. Where are these artifacts stored?',
        },
    ],
    'sc-39': [
        {
            'type': 'process_isolation',
            'question': 'How are processes isolated in AWS (separate AWS accounts, VPC isolation, container isolation, Lambda execution environment isolation, EC2 instance isolation)?',
        },
        {
            'type': 'isolation_enforcement',
            'question': 'How is process isolation enforced (security groups, NACLs, IAM policies, SCPs, container runtime security, hypervisor isolation)?',
        },
        {
            'type': 'isolation_monitoring',
            'question': 'How is isolation monitored (GuardDuty for unusual behavior, VPC Flow Logs, CloudTrail for cross-account access, runtime security monitoring)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-39 compliance? Provide: Account isolation architecture, VPC configurations, container security policies, isolation monitoring reports. Where are these artifacts stored?',
        },
    ],
    'sc-7': [
        {
            'type': 'vpc_architecture',
            'question': 'Describe your VPC architecture: How many VPCs? Are workloads isolated in private subnets? Do you use Transit Gateway or VPC peering for inter-VPC communication?',
        },
        {
            'type': 'traffic_controls',
            'question': 'How is traffic controlled between network segments (security groups, NACLs, AWS Network Firewall)? Are default-deny rules enforced?',
        },
        {
            'type': 'boundary_protection',
            'question': 'What protects your VPC boundaries (NAT Gateways for outbound, ALB/NLB for inbound, WAF for web traffic)? Are VPC Flow Logs enabled and monitored?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-7 compliance in AWS? Provide: AWS Config compliance reports for EC2_SECURITY_GROUP_ATTACHED_TO_ENI, EC2_SECURITY_GROUP_ATTACHED_TO_ENI_PERIODIC, VPC_DEFAULT_SECURITY_GROUP_CLOSED (and 6 more); Security Hub findings for EC2.22, EC2.2, NetworkFirewall.1 (and 3 more); Control Tower compliance status for CONFIG.EC2.DT.11, SH.EC2.22 (and 5 more); Configuration screenshots from AWS Elastic Load Balancing, AWS Network Firewall, Amazon EC2 (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'sc-8': [
        {
            'type': 'encryption_in_transit',
            'question': 'What encryption is required for data in transit (TLS 1.2+ for all connections, HTTPS for APIs, encrypted VPN tunnels)? How is this enforced?',
        },
        {
            'type': 'service_encryption',
            'question': 'Are AWS services configured to use encryption in transit (ALB/NLB with TLS, RDS with SSL, ElastiCache with encryption in transit)? What percentage of traffic is encrypted?',
        },
        {
            'type': 'internal_encryption',
            'question': 'Is encryption required for internal AWS traffic (VPC peering, Transit Gateway, inter-service communication)? Are unencrypted connections blocked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-8 compliance in AWS? Provide: AWS Config compliance reports for ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK, ELB_PREDEFINED_SECURITY_POLICY_SSL_CHECK, ELB_TLS_HTTPS_LISTENERS_ONLY (and 4 more); Security Hub findings for ELB.3, ELB.8, ES.3 (and 3 more); Control Tower compliance status for SH.ELB.3, SH.ELB.8 (and 5 more); Configuration screenshots from AWS Elastic Load Balancing, Amazon OpenSearch Service; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'sc-12': [
        {
            'type': 'key_management_service',
            'question': 'Are you using AWS KMS for cryptographic key management? Are customer-managed keys (CMKs) used instead of AWS-managed keys for sensitive data?',
        },
        {
            'type': 'key_lifecycle',
            'question': 'How are encryption keys managed throughout their lifecycle (generation, rotation, expiration, deletion)? Is automatic key rotation enabled for KMS keys?',
        },
        {
            'type': 'key_access_control',
            'question': 'Who has access to manage and use KMS keys? Are key policies restrictive, and are key usage events logged in CloudTrail?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-12 compliance in AWS? Provide: AWS Config compliance reports for KMS_KEY_POLICY_NO_PUBLIC_ACCESS; Control Tower compliance status for CONFIG.KMS.DT.2, CT.KMS.PR.3 (and 1 more); Configuration screenshots from AWS Key Management Service; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'sc-13': [
        {
            'type': 'cryptographic_standards',
            'question': 'What cryptographic standards are required (AES-256 for encryption, SHA-256 for hashing, RSA-2048+ for keys)? Are weak algorithms prohibited?',
        },
        {
            'type': 'fips_compliance',
            'question': 'Are FIPS 140-2 validated cryptographic modules required? Are you using KMS FIPS endpoints or CloudHSM for FIPS compliance?',
        },
        {
            'type': 'crypto_validation',
            'question': 'How do you validate that only approved cryptography is used (Config rules, automated scanning, code reviews)? Are deprecated algorithms detected and blocked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-13 compliance in AWS? Provide: AWS Config compliance reports for DAX_TLS_ENDPOINT_ENCRYPTION, APPSYNC_CACHE_CT_ENCRYPTION_IN_TRANSIT, EMR_SECURITY_CONFIGURATION_ENCRYPTION_REST; Control Tower compliance status for CONFIG.DAX.DT.1, CONFIG.APPSYNC.DT.3 (and 1 more); Configuration screenshots from AWS AppSync, Amazon DynamoDB Accelerator (DAX), Amazon Elastic MapReduce; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'sc-20': [
        {
            'type': 'authoritative_dns',
            'question': 'Are you operating authoritative DNS servers (Route 53 public hosted zones, on-premises DNS)? If so, is DNSSEC signing enabled to provide authenticated responses?',
        },
        {
            'type': 'dnssec_signing',
            'question': 'For Route 53 hosted zones, have you enabled DNSSEC signing with KMS-managed keys? Are DNSSEC records (RRSIG, DNSKEY) properly configured and monitored?',
        },
        {
            'type': 'dns_integrity',
            'question': 'How do you ensure the integrity of DNS records served to clients? Are zone transfers secured, and is access to modify DNS records restricted and logged?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-20 compliance in AWS? Provide: AWS Config compliance reports for ROUTE53_HOSTED_ZONE_TAGGED; Control Tower compliance status for CONFIG.ROUTE53.DT.2; Configuration screenshots from Amazon Route 53; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'sc-21': [
        {
            'type': 'dnssec_implementation',
            'question': 'Is DNSSEC enabled for your DNS resolution? Are you using Route 53 with DNSSEC signing, or third-party DNS providers with DNSSEC support?',
        },
        {
            'type': 'dns_validation',
            'question': 'Do your DNS resolvers validate DNSSEC signatures to prevent DNS spoofing and cache poisoning? How do you monitor for DNSSEC validation failures?',
        },
        {
            'type': 'dns_protection',
            'question': 'What additional DNS security measures are in place (Route 53 Resolver DNS Firewall, GuardDuty DNS protection, private hosted zones for internal resources)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-21 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED; Security Hub findings for GuardDuty.1; Control Tower compliance status for SH.GuardDuty.1; Configuration screenshots from Amazon GuardDuty, Amazon Route 53; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'sc-28': [
        {
            'type': 'encryption_coverage',
            'question': 'What AWS resources have encryption at rest enabled (S3 buckets, EBS volumes, RDS databases, DynamoDB tables, EFS file systems)? What percentage of resources are encrypted?',
        },
        {
            'type': 'key_management',
            'question': 'How are encryption keys managed (AWS KMS customer-managed keys, AWS-managed keys, CloudHSM)? Who has access to manage and use encryption keys?',
        },
        {
            'type': 'encryption_enforcement',
            'question': 'How do you enforce encryption at rest (SCPs, Config rules, S3 bucket policies requiring encryption)? Are unencrypted resources automatically detected and remediated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-28 compliance in AWS? Provide: AWS Config compliance reports for DYNAMODB_TABLE_ENCRYPTED_KMS, KMS_KEY_POLICY_NO_PUBLIC_ACCESS, ELASTICSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK (and 2 more); Security Hub findings for ES.3, ES.8, Opensearch.3 (and 1 more); Control Tower compliance status for CONFIG.DYNAMODB.DT.4, CT.RDS.PR.16 (and 6 more); Configuration screenshots from AWS Key Management Service, Amazon DynamoDB, Amazon Kinesis Data Streams (and 2 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # System and Information Integrity
    'si-1': [
        {
            'type': 'vulnerability_policy',
            'question': 'What vulnerability management requirements are documented (weekly scanning, 30-day remediation for critical, quarterly penetration testing)? Who is responsible for remediation?',
        },
        {
            'type': 'malware_protection',
            'question': 'What anti-malware solutions are deployed on EC2 instances? Are container images scanned for malware before deployment (ECR image scanning, third-party tools)?',
        },
        {
            'type': 'integrity_monitoring',
            'question': 'How do you monitor for unauthorized changes to AWS resources (CloudTrail, Config, file integrity monitoring on EC2)? Are alerts configured for suspicious activity?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SI-1 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED, INSPECTOR_ENABLED; Security Hub findings for GuardDuty.1; Control Tower compliance status for CONFIG.GUARDDUTY.DT.1, SH.GuardDuty.1; Configuration screenshots from AWS Security Hub, Amazon GuardDuty, Amazon Inspector; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'si-2': [
        {
            'type': 'patch_management',
            'question': 'How are EC2 instances patched (Systems Manager Patch Manager, automated AMI rebuilds, container image updates)? What is your patch SLA for critical vulnerabilities?',
        },
        {
            'type': 'vulnerability_scanning',
            'question': 'What tools scan for vulnerabilities (AWS Inspector for EC2/Lambda/ECR, third-party scanners)? How often do scans run, and who receives the results?',
        },
        {
            'type': 'remediation_tracking',
            'question': 'How are vulnerabilities tracked and remediated? Do you use a ticketing system? What is your process for exceptions or risk acceptance?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SI-2 compliance in AWS? Provide: AWS Config compliance reports for EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK, RDS_AUTOMATIC_MINOR_VERSION_UPGRADE_ENABLED, LAMBDA_FUNCTION_SETTINGS_CHECK; Security Hub findings for SSM.2, RDS.13, Lambda.2; Control Tower compliance status for SH.SSM.2, SH.RDS.13, SH.Lambda.2; Configuration screenshots from AWS Lambda, AWS Systems Manager, Amazon RDS; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'si-3': [
        {
            'type': 'antimalware_deployment',
            'question': 'What anti-malware solutions are deployed (endpoint protection on EC2, GuardDuty for threat detection, Macie for data discovery)? What percentage of instances have protection?',
        },
        {
            'type': 'malware_updates',
            'question': 'How often are anti-malware signatures updated (real-time, daily)? Are updates automated, and how do you verify they are current?',
        },
        {
            'type': 'malware_response',
            'question': 'What happens when malware is detected (automatic quarantine, alert to security team, instance isolation)? Are infected instances automatically removed from service?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SI-3 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_MALWARE_PROTECTION_ENABLED, GUARDDUTY_ENABLED_CENTRALIZED, GUARDDUTY_EKS_PROTECTION_AUDIT_ENABLED; Security Hub findings for GuardDuty.1; Control Tower compliance status for CONFIG.GUARDDUTY.DT.2, SH.GuardDuty.1 (and 1 more); Configuration screenshots from Amazon GuardDuty; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'si-4': [
        {
            'type': 'monitoring_tools',
            'question': 'What tools monitor AWS for security threats (GuardDuty, Security Hub, VPC Flow Logs analysis, CloudWatch anomaly detection)? Are they enabled in all accounts and regions?',
        },
        {
            'type': 'monitoring_coverage',
            'question': 'What is monitored (API calls, network traffic, DNS queries, S3 access patterns, unusual IAM activity)? Are both internal and external threats detected?',
        },
        {
            'type': 'alert_response',
            'question': 'How are security alerts handled (automated response via Lambda, SIEM integration, security team notification)? What is the average time to respond to critical alerts?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SI-4 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_EKS_PROTECTION_RUNTIME_ENABLED, GUARDDUTY_NON_ARCHIVED_FINDINGS, GUARDDUTY_MALWARE_PROTECTION_ENABLED; Control Tower compliance status for CONFIG.GUARDDUTY.DT.7, CONFIG.GUARDDUTY.DT.1 (and 1 more); Configuration screenshots from Amazon GuardDuty; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # Contingency Planning
    'cp-1': [
        {
            'type': 'rto_rpo_requirements',
            'question': 'What are your documented RTO and RPO requirements for critical AWS workloads? How do these drive your backup and DR strategy?',
        },
        {
            'type': 'dr_architecture',
            'question': 'What disaster recovery strategy is implemented (multi-region active-active, pilot light, warm standby, backup and restore)? Which workloads use which strategy?',
        },
        {
            'type': 'testing_procedures',
            'question': 'How often do you test failover and recovery procedures? When was the last DR test, and what were the results?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CP-1 compliance in AWS? Provide: AWS Config compliance reports for BACKUP_RECOVERY_POINT_ENCRYPTED, BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK; Security Hub findings for Backup.1; Control Tower compliance status for BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK; Configuration screenshots from AWS Backup, Amazon DynamoDB, Amazon RDS (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cp-2': [
        {
            'type': 'contingency_plan_content',
            'question': 'Do you have documented contingency plans for each critical AWS workload? Do they include recovery procedures, contact information, and dependencies?',
        },
        {
            'type': 'plan_maintenance',
            'question': 'How often are contingency plans reviewed and updated? Are they updated when architecture changes or new services are deployed?',
        },
        {
            'type': 'plan_distribution',
            'question': 'Where are contingency plans stored, and who has access? Are they accessible during an outage (stored outside AWS, printed copies)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CP-2 compliance in AWS? Provide: AWS Config compliance reports for BACKUP_RECOVERY_POINT_ENCRYPTED, BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK, EFS_IN_BACKUP_PLAN (and 1 more); Security Hub findings for Backup.1, EFS.2; Control Tower compliance status for BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK, CONFIG.ELASTICFILESYSTEM.DT.4 (and 2 more); Configuration screenshots from AWS Backup, Amazon Elastic File System; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cp-4': [
        {
            'type': 'testing_frequency',
            'question': 'How often do you test contingency plans (annually, semi-annually, after major changes)? What types of tests are conducted (tabletop, functional, full failover)?',
        },
        {
            'type': 'testing_scope',
            'question': 'What is tested during contingency exercises (failover to DR region, backup restoration, communication procedures, runbook accuracy)?',
        },
        {
            'type': 'testing_results',
            'question': 'How are test results documented and lessons learned captured? What improvements were made after the last contingency test?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CP-4 compliance in AWS? Provide: AWS Config compliance reports for AURORA_LAST_BACKUP_RECOVERY_POINT_CREATED, VIRTUALMACHINE_LAST_BACKUP_RECOVERY_POINT_CREATED, BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED; Control Tower compliance status for AURORA_LAST_BACKUP_RECOVERY_POINT_CREATED, CONFIG.BACKUP-GATEWAY.DT.3 (and 1 more); Configuration screenshots from AWS Backup, Amazon RDS; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'cp-9': [
        {
            'type': 'backup_coverage',
            'question': 'What AWS resources are backed up (EBS snapshots, RDS automated backups, S3 versioning, DynamoDB backups)? Are you using AWS Backup for centralized management?',
        },
        {
            'type': 'backup_protection',
            'question': 'How are backups protected (encryption with KMS, cross-region replication, AWS Backup Vault Lock for immutability)? Are backups in a separate AWS account?',
        },
        {
            'type': 'restore_testing',
            'question': 'How often are restore procedures tested? When was the last successful restore? What is the average restore time for critical systems?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CP-9 compliance in AWS? Provide: AWS Config compliance reports for EBS_IN_BACKUP_PLAN, EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN, S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN (and 2 more); Security Hub findings for EC2.28, Backup.1; Control Tower compliance status for CONFIG.EC2.DT.14, CONFIG.EC2.DT.6 (and 3 more); Configuration screenshots from AWS Backup, Amazon Elastic Block Store, Amazon RDS (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # Incident Response
    'ir-1': [
        {
            'type': 'incident_procedures',
            'question': 'What incident response procedures are documented for AWS security events? Are roles defined (incident commander, technical lead, communications)?',
        },
        {
            'type': 'detection_integration',
            'question': 'How are AWS security alerts integrated into your incident response process (GuardDuty findings, Security Hub alerts, CloudWatch alarms)? What triggers a formal incident?',
        },
        {
            'type': 'escalation_procedures',
            'question': 'What are the escalation procedures for AWS security incidents? When do you engage AWS Support, and do you have an AWS Enterprise Support plan?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates IR-1 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1; Configuration screenshots from AWS Security Hub, Amazon EventBridge; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ir-4': [
        {
            'type': 'detection_capabilities',
            'question': 'What tools detect security incidents in AWS (GuardDuty, Security Hub, CloudWatch anomaly detection, third-party SIEM)? How are alerts triaged and prioritized?',
        },
        {
            'type': 'response_runbooks',
            'question': 'Are incident response runbooks documented for common AWS scenarios (compromised IAM credentials, S3 bucket exposure, EC2 instance compromise)? Where are they stored?',
        },
        {
            'type': 'incident_testing',
            'question': 'How often do you conduct incident response exercises or tabletop drills for AWS scenarios? When was the last one, and what improvements were identified?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates IR-4 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED, GUARDDUTY_NON_ARCHIVED_FINDINGS, SECURITYHUB_ENABLED (and 1 more); Security Hub findings for GuardDuty.1, CloudWatch.17; Control Tower compliance status for CONFIG.GUARDDUTY.DT.1, SH.GuardDuty.1 (and 1 more); Configuration screenshots from AWS Security Hub, Amazon CloudWatch, Amazon GuardDuty; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ir-8': [
        {
            'type': 'plan_existence',
            'question': 'Do you have a documented incident response plan that covers AWS security incidents? Does it define incident categories, severity levels, and response procedures?',
        },
        {
            'type': 'plan_content',
            'question': 'Does your IR plan include AWS-specific procedures (isolating compromised instances, revoking IAM credentials, analyzing CloudTrail logs, engaging AWS Support)?',
        },
        {
            'type': 'plan_maintenance',
            'question': 'How often is the incident response plan reviewed and updated? Is it updated when new AWS services are deployed or architecture changes?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates IR-8 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED, CLOUDTRAIL_SECURITY_TRAIL_ENABLED, BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED; Security Hub findings for CloudTrail.3; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1, CONFIG.CLOUDTRAIL.DT.6 (and 1 more); Configuration screenshots from AWS Backup, AWS CloudTrail, AWS Security Hub; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    
    # Planning
    'pl-1': [
        {
            'type': 'security_planning',
            'question': 'How is security incorporated into AWS architecture decisions? Do you require security reviews before deploying new workloads or making significant changes?',
        },
        {
            'type': 'well_architected',
            'question': 'Do you use the AWS Well-Architected Framework for security planning? How many Well-Architected Reviews have been conducted, and how are findings tracked?',
        },
        {
            'type': 'security_requirements',
            'question': 'How are security requirements documented for new AWS projects (threat models, data classification, compliance requirements)? Who approves security designs?',
        },
    ],
    
    # Risk Assessment
    'ra-1': [
        {
            'type': 'risk_assessment_process',
            'question': 'How often are risk assessments conducted for AWS environments (annually, after major changes, continuous monitoring)? Who conducts them?',
        },
        {
            'type': 'aws_specific_risks',
            'question': 'What AWS-specific risks are assessed (misconfigurations, excessive IAM permissions, public S3 buckets, unencrypted data, compliance violations)? What tools support this?',
        },
        {
            'type': 'risk_remediation',
            'question': 'How are identified risks tracked and remediated? Do you use a risk register? What is the process for accepting risks that cannot be immediately remediated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates RA-1 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1; Configuration screenshots from AWS Security Hub, AWS Trusted Advisor; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
        },
    ],
    'ra-5': [
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
# Assessment, Authorization, and Monitoring (CA)
    'ca-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented policies for security assessment, authorization, and continuous monitoring in AWS? Does it define assessment frequency, authorization requirements, and monitoring scope?',
        },
        {
            'type': 'aws_assessment_tools',
            'question': 'Does your policy specify which AWS assessment tools to use (Security Hub, Config, Inspector, Trusted Advisor, Audit Manager)? Are assessment procedures documented?',
        },
        {
            'type': 'authorization_process',
            'question': 'What is your AWS system authorization process (initial ATO, continuous ATO, reauthorization frequency)? Who is the authorizing official for AWS workloads?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-1 compliance? Provide: Assessment and authorization policy document with approval signatures, policy review records, assessment procedure documentation. Where are these artifacts stored?',
        },
    ],
    'ca-2': [
        {
            'type': 'assessment_frequency',
            'question': 'How often are security control assessments conducted in AWS (annually, continuously, after major changes)? Are you using AWS Audit Manager for continuous assessment?',
        },
        {
            'type': 'assessment_scope',
            'question': 'What is assessed (IAM policies, network configurations, encryption settings, logging, monitoring, incident response capabilities)? Do assessments cover all AWS accounts and regions?',
        },
        {
            'type': 'assessment_tools',
            'question': 'What tools support control assessments (Security Hub security standards, Config conformance packs, Inspector assessments, manual reviews)? Are findings tracked in a centralized system?',
        },
        {
            'type': 'independent_assessors',
            'question': 'Are assessments conducted by independent assessors (third-party auditors, internal audit team separate from operations)? How is assessor independence verified?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-2 compliance? Provide: Assessment reports, Security Hub compliance summaries, Config conformance pack results, assessment schedules, assessor qualifications. Where are these artifacts stored?',
        },
    ],
    'ca-3': [
        {
            'type': 'connection_authorization',
            'question': 'What is your process for authorizing connections between AWS and external systems (VPN, Direct Connect, VPC peering, Transit Gateway, third-party SaaS)? Who approves these connections?',
        },
        {
            'type': 'security_requirements',
            'question': 'What security requirements must external connections meet (encryption in transit, authentication, logging, data classification restrictions)? How are requirements enforced?',
        },
        {
            'type': 'connection_monitoring',
            'question': 'How are external connections monitored (VPC Flow Logs, CloudWatch metrics, GuardDuty findings, third-party network monitoring)? Are unauthorized connections detected and blocked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-3 compliance? Provide: Connection authorization documentation, security requirements for external connections, VPC Flow Logs, network diagrams, connection monitoring reports. Where are these artifacts stored?',
        },
    ],
    'ca-5': [
        {
            'type': 'poam_process',
            'question': 'Do you maintain a Plan of Action and Milestones (POA&M) for AWS security findings? What tool tracks remediation (JIRA, ServiceNow, AWS Security Hub, spreadsheet)?',
        },
        {
            'type': 'finding_sources',
            'question': 'What sources feed into your POA&M (Security Hub findings, Config non-compliance, Inspector vulnerabilities, penetration test results, audit findings)? How are findings prioritized?',
        },
        {
            'type': 'remediation_tracking',
            'question': 'What are your remediation SLAs by severity (critical: 7 days, high: 30 days, medium: 90 days)? How often is POA&M status reviewed with management?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-5 compliance? Provide: Current POA&M with all open findings, remediation status reports, management review meeting notes, closed finding documentation. Where are these artifacts stored?',
        },
    ],
    'ca-6': [
        {
            'type': 'authorization_process',
            'question': 'What is your AWS system authorization process? Do you have an Authority to Operate (ATO) for your AWS environment? When does it expire, and what triggers reauthorization?',
        },
        {
            'type': 'authorization_package',
            'question': 'What is included in your authorization package (system security plan, risk assessment, control assessment results, POA&M, authorization decision letter)? Is it updated regularly?',
        },
        {
            'type': 'authorizing_official',
            'question': 'Who is the Authorizing Official for AWS systems? Do they have appropriate authority level and independence from system operations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-6 compliance? Provide: Current authorization decision letter, system security plan, authorization package documentation, reauthorization schedule. Where are these artifacts stored?',
        },
    ],
    'ca-7': [
        {
            'type': 'monitoring_strategy',
            'question': 'What is your continuous monitoring strategy for AWS (Security Hub, Config, GuardDuty, CloudWatch, CloudTrail)? Are all AWS accounts and regions monitored?',
        },
        {
            'type': 'monitoring_scope',
            'question': 'What is monitored (configuration changes, security findings, compliance status, vulnerabilities, threats, user activity, network traffic)? How frequently are findings reviewed?',
        },
        {
            'type': 'automated_response',
            'question': 'Do you have automated responses to monitoring findings (Lambda remediation, Systems Manager automation, Security Hub custom actions, EventBridge rules)? What findings trigger automatic remediation?',
        },
        {
            'type': 'reporting',
            'question': 'How often are monitoring results reported to management (daily dashboards, weekly summaries, monthly reports)? Who receives these reports, and what actions result?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-7 compliance? Provide: Security Hub dashboards, Config compliance timelines, GuardDuty findings reports, monitoring strategy document, management review records. Where are these artifacts stored?',
        },
    ],
    'ca-9': [
        {
            'type': 'internal_connections',
            'question': 'What internal connections exist in your AWS environment (VPC peering, Transit Gateway, PrivateLink, cross-account access)? Are they documented and authorized?',
        },
        {
            'type': 'connection_security',
            'question': 'How are internal connections secured (security groups, NACLs, IAM policies, resource policies, SCPs)? Are least privilege principles applied?',
        },
        {
            'type': 'connection_monitoring',
            'question': 'How are internal connections monitored (VPC Flow Logs, CloudTrail, Config rules for unauthorized connections)? Are connection changes alerted?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-9 compliance? Provide: Network architecture diagrams, connection authorization records, VPC Flow Logs, security group configurations, monitoring alerts. Where are these artifacts stored?',
        },
    ],
    
    # System and Services Acquisition (SA)
    'sa-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented policies for acquiring and developing systems in AWS? Does it cover security requirements, vendor assessment, and secure development practices?',
        },
        {
            'type': 'aws_service_selection',
            'question': 'Does your policy define criteria for selecting AWS services (compliance certifications, data residency, encryption capabilities, audit logging)? Who approves new AWS service usage?',
        },
        {
            'type': 'third_party_services',
            'question': 'What is your process for evaluating third-party services that integrate with AWS (security assessment, contract review, data protection requirements)? Are approved services documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-1 compliance? Provide: System acquisition policy document with approval signatures, AWS service approval process, approved services list, policy review records. Where are these artifacts stored?',
        },
    ],
    'sa-2': [
        {
            'type': 'resource_allocation',
            'question': 'How do you allocate resources for AWS security (budget for security tools, staff for security operations, time for security reviews)? Is security funding adequate?',
        },
        {
            'type': 'security_budget',
            'question': 'What security tools and services are funded (Security Hub, GuardDuty, Inspector, Macie, third-party tools)? Are security costs tracked separately from infrastructure costs?',
        },
        {
            'type': 'staffing',
            'question': 'Do you have dedicated AWS security staff or is it shared responsibility? What is the ratio of security staff to AWS accounts/workloads?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-2 compliance? Provide: Security budget documentation, security tool subscriptions, staffing plans, resource allocation decisions. Where are these artifacts stored?',
        },
    ],
    'sa-3': [
        {
            'type': 'sdlc_process',
            'question': 'What is your secure development lifecycle for AWS applications? Does it include threat modeling, secure coding, security testing, and deployment reviews?',
        },
        {
            'type': 'security_gates',
            'question': 'What security gates exist in your SDLC (design review, code review, SAST/DAST scanning, penetration testing, security approval before production)? Can deployments be blocked for security issues?',
        },
        {
            'type': 'infrastructure_as_code',
            'question': 'Do you use Infrastructure as Code for AWS deployments (CloudFormation, Terraform, CDK)? Are IaC templates scanned for security issues (Checkov, cfn-nag, Terraform Sentinel)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-3 compliance? Provide: SDLC documentation, security gate requirements, IaC scanning reports, code review records, security approval documentation. Where are these artifacts stored?',
        },
    ],
    'sa-4': [
        {
            'type': 'acquisition_requirements',
            'question': 'What security requirements are included in AWS service and third-party acquisitions (encryption, logging, compliance certifications, data residency, incident response)?',
        },
        {
            'type': 'vendor_assessment',
            'question': 'How do you assess third-party vendors that integrate with AWS (security questionnaires, SOC 2 reports, penetration test results, compliance certifications)? Who approves vendors?',
        },
        {
            'type': 'contract_requirements',
            'question': 'What security clauses are in vendor contracts (data protection, breach notification, audit rights, data deletion, subprocessor restrictions)? Are contracts reviewed by legal and security?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-4 compliance? Provide: Security requirements documentation, vendor assessment reports, approved vendor list, contract security clauses, vendor compliance certificates. Where are these artifacts stored?',
        },
    ],
    'sa-5': [
        {
            'type': 'system_documentation',
            'question': 'What documentation exists for AWS systems (architecture diagrams, data flow diagrams, security controls, configuration standards, runbooks)? Is it kept current?',
        },
        {
            'type': 'documentation_location',
            'question': 'Where is AWS system documentation stored (wiki, SharePoint, Git repository, AWS Systems Manager documents)? Who has access, and how is it version controlled?',
        },
        {
            'type': 'documentation_updates',
            'question': 'How often is documentation reviewed and updated (after changes, quarterly, annually)? Who is responsible for maintaining documentation accuracy?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-5 compliance? Provide: System architecture diagrams, security control documentation, configuration standards, documentation update logs, documentation access controls. Where are these artifacts stored?',
        },
    ],
    'sa-8': [
        {
            'type': 'security_principles',
            'question': 'What security engineering principles guide AWS architecture (defense in depth, least privilege, separation of duties, fail secure, complete mediation)? Are they documented?',
        },
        {
            'type': 'well_architected',
            'question': 'Do you follow the AWS Well-Architected Framework security pillar? Have you conducted Well-Architected Reviews? How are findings addressed?',
        },
        {
            'type': 'security_by_design',
            'question': 'How is security incorporated into design decisions (threat modeling, security architecture review, security requirements in design documents)? Who reviews designs for security?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-8 compliance? Provide: Security engineering principles documentation, Well-Architected Review reports, threat models, security architecture review records. Where are these artifacts stored?',
        },
    ],
    'sa-9': [
        {
            'type': 'external_services',
            'question': 'What external services integrate with your AWS environment (SaaS applications, third-party APIs, managed services, data processors)? Are they inventoried and approved?',
        },
        {
            'type': 'service_security',
            'question': 'How do you ensure external services meet security requirements (SOC 2 Type II, ISO 27001, security assessments, contract terms)? Are services reassessed periodically?',
        },
        {
            'type': 'data_protection',
            'question': 'How is data protected when shared with external services (encryption in transit, data minimization, access controls, data residency requirements)? Are data flows documented?',
        },
        {
            'type': 'monitoring',
            'question': 'How are external service connections monitored (API logging, CloudTrail for AWS service integrations, anomaly detection)? Are unauthorized connections detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-9 compliance? Provide: External services inventory, service security assessments, data flow diagrams, service contracts, monitoring logs. Where are these artifacts stored?',
        },
    ],
    'sa-10': [
        {
            'type': 'configuration_management',
            'question': 'How do you manage AWS infrastructure configurations (Git for IaC, AWS Config for drift detection, version control for CloudFormation/Terraform)? Are changes tracked and auditable?',
        },
        {
            'type': 'change_control',
            'question': 'What is your change control process for AWS infrastructure (pull requests, peer review, automated testing, approval workflow)? Can unauthorized changes be prevented?',
        },
        {
            'type': 'baseline_configurations',
            'question': 'Do you have baseline configurations for AWS resources (EC2 AMIs, security group templates, IAM policy templates)? How are baselines enforced and deviations detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-10 compliance? Provide: IaC repository with change history, Config drift detection reports, baseline configuration documentation, change approval records. Where are these artifacts stored?',
        },
    ],
    'sa-11': [
        {
            'type': 'security_testing',
            'question': 'What security testing is performed before AWS deployments (SAST, DAST, dependency scanning, IaC security scanning, penetration testing)? Are tests automated in CI/CD?',
        },
        {
            'type': 'testing_frequency',
            'question': 'How often is security testing conducted (every commit, every release, quarterly, annually)? Are critical findings blocking deployments?',
        },
        {
            'type': 'testing_tools',
            'question': 'What tools support security testing (SonarQube, Snyk, Checkmarx, OWASP ZAP, AWS Inspector, third-party scanners)? Are findings tracked and remediated?',
        },
        {
            'type': 'penetration_testing',
            'question': 'How often are penetration tests conducted on AWS environments (annually, after major changes)? Are AWS penetration testing guidelines followed? Who conducts tests?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-11 compliance? Provide: Security testing reports, SAST/DAST scan results, penetration test reports, testing schedule, remediation tracking. Where are these artifacts stored?',
        },
    ],
    'sa-15': [
        {
            'type': 'development_standards',
            'question': 'What secure development standards apply to AWS applications (OWASP Top 10, AWS security best practices, coding standards, security libraries)? Are developers trained on these standards?',
        },
        {
            'type': 'development_tools',
            'question': 'What development tools enforce security (IDE security plugins, pre-commit hooks, automated code review, security linters)? Are insecure practices prevented?',
        },
        {
            'type': 'code_review',
            'question': 'Are security-focused code reviews required (peer review, security team review for sensitive changes)? What security issues are reviewers trained to identify?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-15 compliance? Provide: Secure development standards documentation, code review records, security training completion, development tool configurations. Where are these artifacts stored?',
        },
    ],
    'sa-22': [
        {
            'type': 'unsupported_components',
            'question': 'How do you identify unsupported components in AWS (EOL operating systems, deprecated AWS services, unmaintained libraries)? Are they inventoried?',
        },
        {
            'type': 'replacement_plan',
            'question': 'What is your plan for replacing unsupported components (migration timeline, alternative solutions, risk acceptance for delays)? Who approves continued use of unsupported components?',
        },
        {
            'type': 'monitoring',
            'question': 'How are unsupported components monitored for vulnerabilities (Inspector scanning, manual tracking, vendor notifications)? Are compensating controls in place?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-22 compliance? Provide: Unsupported components inventory, replacement plans, risk acceptance documentation, vulnerability monitoring reports. Where are these artifacts stored?',
        },
    ],
    
    # Personnel Security (PS)
    'ps-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented personnel security policies covering position risk designation, screening, termination, and access agreements? When was it last reviewed?',
        },
        {
            'type': 'aws_access_controls',
            'question': 'Does your policy address AWS-specific personnel security (IAM user lifecycle, privileged access management, access reviews, separation of duties)?',
        },
        {
            'type': 'policy_enforcement',
            'question': 'How is your personnel security policy enforced (HR processes, IAM automation, access review workflows, termination checklists)? Are violations tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-1 compliance? Provide: Personnel security policy document with approval signatures, policy review records, enforcement procedure documentation. Where are these artifacts stored?',
        },
    ],
    'ps-2': [
        {
            'type': 'position_designation',
            'question': 'Have you designated risk levels for positions with AWS access (high risk for admins, moderate for developers, low for read-only users)? Is this documented?',
        },
        {
            'type': 'screening_requirements',
            'question': 'What screening requirements apply to each risk level (background checks, reference checks, education verification)? Are requirements based on position sensitivity?',
        },
        {
            'type': 'reassessment',
            'question': 'How often are position risk designations reassessed (when duties change, annually, when access level changes)? Who approves risk designations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-2 compliance? Provide: Position risk designation documentation, screening requirements by risk level, reassessment records. Where are these artifacts stored?',
        },
    ],
    'ps-3': [
        {
            'type': 'screening_process',
            'question': 'What screening is conducted before granting AWS access (background checks, employment verification, reference checks, education verification)? Who conducts screening?',
        },
        {
            'type': 'screening_criteria',
            'question': 'What are the screening criteria for AWS privileged access (criminal background check, credit check for financial systems, citizenship requirements)? Are criteria risk-based?',
        },
        {
            'type': 'rescreening',
            'question': 'How often is rescreening conducted (every 5 years, when position changes, when access level increases)? Are rescreening requirements documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-3 compliance? Provide: Screening procedure documentation, background check records (redacted), screening completion records, rescreening schedule. Where are these artifacts stored?',
        },
    ],
    'ps-4': [
        {
            'type': 'termination_process',
            'question': 'What is your process for terminating AWS access when employees leave (immediate IAM user disablement, access key deletion, MFA device removal, session revocation)? How quickly is it executed?',
        },
        {
            'type': 'termination_checklist',
            'question': 'Do you have a termination checklist for AWS access (disable IAM user, remove from groups, delete access keys, remove MFA, review CloudTrail for final actions)? Who verifies completion?',
        },
        {
            'type': 'knowledge_transfer',
            'question': 'How is AWS knowledge transferred when personnel leave (documentation handoff, access to runbooks, credential rotation, system ownership transfer)? Is this tracked?',
        },
        {
            'type': 'post_termination_review',
            'question': 'Are terminated user activities reviewed post-termination (CloudTrail logs, resource changes, data access)? How long are logs retained for this purpose?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-4 compliance? Provide: Termination checklist, IAM user termination records, CloudTrail logs of termination actions, knowledge transfer documentation. Where are these artifacts stored?',
        },
    ],
    'ps-5': [
        {
            'type': 'transfer_process',
            'question': 'What is your process when personnel transfer to new roles (access review, privilege adjustment, new role training, knowledge transfer)? How quickly is access adjusted?',
        },
        {
            'type': 'access_adjustment',
            'question': 'How are AWS permissions adjusted during transfers (remove old role permissions, add new role permissions, review for least privilege)? Is this automated or manual?',
        },
        {
            'type': 'transfer_review',
            'question': 'Who reviews and approves access changes during transfers (new manager, security team, HR)? Are approvals documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-5 compliance? Provide: Transfer procedure documentation, access change records, approval documentation, IAM policy change logs. Where are these artifacts stored?',
        },
    ],
    'ps-6': [
        {
            'type': 'access_agreements',
            'question': 'Do personnel sign access agreements before receiving AWS access (acceptable use policy, confidentiality agreement, security responsibilities)? Are agreements reviewed annually?',
        },
        {
            'type': 'agreement_content',
            'question': 'What do access agreements cover (data protection, password security, MFA requirements, prohibited activities, incident reporting, acceptable use)?',
        },
        {
            'type': 'nda_requirements',
            'question': 'Are NDAs required for personnel with access to sensitive AWS data? Are third-party contractors required to sign additional agreements?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-6 compliance? Provide: Access agreement templates, signed agreements (redacted), annual review records, contractor agreements. Where are these artifacts stored?',
        },
    ],
    'ps-7': [
        {
            'type': 'third_party_requirements',
            'question': 'What security requirements apply to third-party personnel with AWS access (background checks, security training, access agreements, supervision requirements)?',
        },
        {
            'type': 'contractor_management',
            'question': 'How are contractors and third-party personnel managed in AWS (separate IAM accounts, time-limited access, activity monitoring, access reviews)? Are they clearly identified?',
        },
        {
            'type': 'third_party_termination',
            'question': 'How is third-party access terminated when contracts end (automated expiration, manual review, access key deletion)? Who verifies termination?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-7 compliance? Provide: Third-party security requirements, contractor IAM accounts list, access termination records, monitoring reports. Where are these artifacts stored?',
        },
    ],
    'ps-8': [
        {
            'type': 'sanctions_policy',
            'question': 'Do you have a personnel sanctions policy for security violations (policy violations, unauthorized access, data breaches, negligence)? What are the consequences?',
        },
        {
            'type': 'violation_tracking',
            'question': 'How are security violations tracked and investigated (incident tickets, HR cases, CloudTrail analysis)? Who investigates violations?',
        },
        {
            'type': 'sanctions_process',
            'question': 'What is the sanctions process (warning, suspension, termination, legal action)? Are sanctions proportional to violation severity? Who approves sanctions?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-8 compliance? Provide: Personnel sanctions policy, violation tracking records (redacted), sanctions decisions (redacted), policy communication records. Where are these artifacts stored?',
        },
    ],
    'ps-9': [
        {
            'type': 'position_descriptions',
            'question': 'Do position descriptions for AWS roles include security responsibilities (least privilege, MFA usage, incident reporting, security training, acceptable use)?',
        },
        {
            'type': 'security_roles',
            'question': 'Are security roles and responsibilities clearly defined (security team, system administrators, developers, auditors)? Do job descriptions reflect actual AWS access levels?',
        },
        {
            'type': 'role_review',
            'question': 'How often are position descriptions reviewed and updated (annually, when duties change, when new AWS services are adopted)? Who approves updates?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-9 compliance? Provide: Position descriptions with security responsibilities, role definition documentation, review and update records. Where are these artifacts stored?',
        },
    ],
    
    # Maintenance (MA)
    'ma-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented maintenance policies for AWS systems (patching, updates, maintenance windows, emergency maintenance)? When was it last reviewed?',
        },
        {
            'type': 'aws_maintenance',
            'question': 'Does your policy address AWS-specific maintenance (Systems Manager Patch Manager, automated patching, AMI updates, Lambda runtime updates, RDS maintenance windows)?',
        },
        {
            'type': 'maintenance_windows',
            'question': 'Are maintenance windows defined for AWS resources? How are maintenance activities scheduled and communicated? Are emergency patches expedited?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-1 compliance? Provide: Maintenance policy document with approval signatures, maintenance schedule, policy review records. Where are these artifacts stored?',
        },
    ],
    'ma-2': [
        {
            'type': 'maintenance_control',
            'question': 'How is AWS maintenance controlled (change management, approval workflows, maintenance windows, rollback procedures)? Who approves maintenance activities?',
        },
        {
            'type': 'maintenance_logging',
            'question': 'Are maintenance activities logged (CloudTrail for API calls, Systems Manager maintenance windows, change tickets)? How long are maintenance logs retained?',
        },
        {
            'type': 'maintenance_review',
            'question': 'Are maintenance activities reviewed post-completion (success verification, rollback if needed, lessons learned)? Who conducts reviews?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-2 compliance? Provide: Maintenance approval records, CloudTrail logs of maintenance activities, maintenance window reports, post-maintenance reviews. Where are these artifacts stored?',
        },
    ],
    'ma-3': [
        {
            'type': 'maintenance_tools',
            'question': 'What tools are used for AWS maintenance (Systems Manager, third-party patch management, automation scripts)? Are tools approved and secured?',
        },
        {
            'type': 'tool_security',
            'question': 'How are maintenance tools secured (IAM roles with least privilege, MFA for access, audit logging, tool integrity verification)? Are tools regularly updated?',
        },
        {
            'type': 'tool_inspection',
            'question': 'Are maintenance tools inspected for security issues (vulnerability scanning, code review for custom scripts, vendor security assessments)? How often?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-3 compliance? Provide: Approved maintenance tools list, tool security configurations, tool inspection reports, IAM policies for maintenance tools. Where are these artifacts stored?',
        },
    ],
    'ma-4': [
        {
            'type': 'nonlocal_maintenance',
            'question': 'How is remote maintenance of AWS resources controlled (VPN requirements, MFA, session recording, approval workflows)? Are remote sessions monitored?',
        },
        {
            'type': 'remote_access_tools',
            'question': 'What tools enable remote AWS maintenance (Systems Manager Session Manager, AWS Client VPN, third-party remote access)? Are sessions encrypted and logged?',
        },
        {
            'type': 'third_party_maintenance',
            'question': 'If third parties perform remote maintenance, how is access controlled (time-limited IAM roles, supervised sessions, activity logging)? Are third-party actions reviewed?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-4 compliance? Provide: Remote maintenance procedure documentation, Session Manager logs, VPN access logs, third-party maintenance records. Where are these artifacts stored?',
        },
    ],
    'ma-5': [
        {
            'type': 'maintenance_personnel',
            'question': 'Who is authorized to perform AWS maintenance (system administrators, DevOps team, third-party vendors)? Is authorization documented and reviewed?',
        },
        {
            'type': 'personnel_supervision',
            'question': 'Are maintenance personnel supervised during sensitive activities (production changes, security configuration updates, data access)? Who provides supervision?',
        },
        {
            'type': 'personnel_screening',
            'question': 'What screening is required for maintenance personnel (background checks, security training, access agreements)? Are requirements risk-based?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-5 compliance? Provide: Authorized maintenance personnel list, supervision records, personnel screening documentation, IAM access records. Where are these artifacts stored?',
        },
    ],
    'ma-6': [
        {
            'type': 'timely_maintenance',
            'question': 'How quickly are security patches applied to AWS resources (critical: 7 days, high: 30 days, medium: 90 days)? Are SLAs documented and tracked?',
        },
        {
            'type': 'patch_management',
            'question': 'What is your AWS patch management process (Systems Manager Patch Manager, automated patching, patch testing, rollback procedures)? Are all resource types covered?',
        },
        {
            'type': 'maintenance_tracking',
            'question': 'How is maintenance compliance tracked (Systems Manager compliance reports, Config rules, third-party tools)? Are overdue patches escalated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-6 compliance? Provide: Patch management SLAs, Systems Manager compliance reports, patch deployment records, overdue patch reports. Where are these artifacts stored?',
        },
    ],
    
    # Media Protection (MP)
    'mp-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented media protection policies for AWS (data classification, encryption requirements, data disposal, backup protection)? When was it last reviewed?',
        },
        {
            'type': 'aws_data_protection',
            'question': 'Does your policy address AWS-specific media protection (S3 encryption, EBS encryption, RDS encryption, backup encryption, data lifecycle management)?',
        },
        {
            'type': 'data_classification',
            'question': 'Do you have a data classification scheme (public, internal, confidential, restricted)? Are AWS resources tagged with data classification? How is classification enforced?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-1 compliance? Provide: Media protection policy document with approval signatures, data classification scheme, policy review records. Where are these artifacts stored?',
        },
    ],
    'mp-2': [
        {
            'type': 'media_access',
            'question': 'How is access to AWS data storage controlled (S3 bucket policies, EBS volume encryption, IAM policies, resource policies)? Is least privilege enforced?',
        },
        {
            'type': 'access_logging',
            'question': 'Are data access activities logged (S3 access logging, CloudTrail data events, VPC Flow Logs for EBS)? How long are access logs retained?',
        },
        {
            'type': 'unauthorized_access',
            'question': 'How is unauthorized data access detected and prevented (GuardDuty, Macie, Config rules for public access, automated remediation)? Are alerts configured?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-2 compliance? Provide: S3 bucket policies, IAM access policies, access logging configurations, GuardDuty findings, unauthorized access alerts. Where are these artifacts stored?',
        },
    ],
    'mp-3': [
        {
            'type': 'media_marking',
            'question': 'How is AWS data marked with classification (resource tags, S3 object tags, metadata)? Are classification tags required and enforced?',
        },
        {
            'type': 'marking_automation',
            'question': 'Is data classification marking automated (Lambda functions, Config rules, tag policies)? How are untagged resources detected?',
        },
        {
            'type': 'marking_validation',
            'question': 'How is classification marking validated (Config rules, automated scanning, periodic reviews)? Are incorrectly marked resources corrected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-3 compliance? Provide: Tagging standards documentation, resource tag reports, untagged resource reports, tag enforcement policies. Where are these artifacts stored?',
        },
    ],
    'mp-4': [
        {
            'type': 'media_storage',
            'question': 'How is AWS data stored securely (encryption at rest, access controls, network isolation, backup encryption)? Are storage security requirements documented?',
        },
        {
            'type': 'encryption_requirements',
            'question': 'What encryption is required for AWS storage (S3 default encryption, EBS encryption, RDS encryption, KMS key management)? Are encryption requirements enforced?',
        },
        {
            'type': 'storage_monitoring',
            'question': 'How is storage security monitored (Config rules for encryption, Macie for sensitive data, Security Hub findings)? Are unencrypted resources detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-4 compliance? Provide: Storage encryption configurations, Config compliance reports, KMS key policies, storage security monitoring reports. Where are these artifacts stored?',
        },
    ],
    'mp-5': [
        {
            'type': 'media_transport',
            'question': 'How is data protected during transport to/from AWS (TLS/SSL, VPN, Direct Connect with MACsec, AWS Transfer Family with encryption)? Are transport security requirements documented?',
        },
        {
            'type': 'transport_encryption',
            'question': 'Is encryption in transit enforced (S3 bucket policies requiring SSL, ALB/NLB with TLS, API Gateway with TLS)? Are weak protocols blocked?',
        },
        {
            'type': 'transport_monitoring',
            'question': 'How is data transport monitored (VPC Flow Logs, CloudTrail, GuardDuty for unusual data transfers)? Are unencrypted transfers detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-5 compliance? Provide: Transport encryption configurations, S3 bucket policies requiring SSL, VPC Flow Logs, transport security monitoring reports. Where are these artifacts stored?',
        },
    ],
    'mp-6': [
        {
            'type': 'media_sanitization',
            'question': 'What is your process for sanitizing AWS data before disposal (S3 object deletion with versioning disabled, EBS volume deletion, RDS snapshot deletion, KMS key deletion)?',
        },
        {
            'type': 'sanitization_verification',
            'question': 'How do you verify data sanitization (CloudTrail logs of deletion, Config rules for deleted resources, automated verification)? Are deletion activities logged?',
        },
        {
            'type': 'aws_responsibility',
            'question': 'Do you acknowledge AWS responsibility for physical media sanitization in their data centers? Have you reviewed AWS data destruction procedures in AWS Artifact?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-6 compliance? Provide: Data sanitization procedures, CloudTrail logs of deletion activities, sanitization verification records, AWS Artifact data destruction documentation. Where are these artifacts stored?',
        },
    ],
    'mp-7': [
        {
            'type': 'media_use',
            'question': 'Are there restrictions on AWS data usage (data classification-based access, purpose limitations, geographic restrictions)? How are restrictions enforced?',
        },
        {
            'type': 'usage_monitoring',
            'question': 'How is data usage monitored (CloudTrail data events, S3 access logging, Macie for sensitive data access, GuardDuty for anomalous access)? Are violations detected?',
        },
        {
            'type': 'usage_restrictions',
            'question': 'What technical controls enforce usage restrictions (IAM policies, S3 bucket policies, SCPs, VPC endpoints, PrivateLink)? Are controls tested?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-7 compliance? Provide: Data usage restriction policies, IAM policies enforcing restrictions, usage monitoring reports, violation alerts. Where are these artifacts stored?',
        },
    ],
    'mp-8': [
        {
            'type': 'media_downgrading',
            'question': 'What is your process for downgrading AWS data classification (review and approval, metadata updates, access control changes)? Who approves downgrading?',
        },
        {
            'type': 'downgrading_verification',
            'question': 'How is data downgrading verified (tag updates, policy changes, access reviews)? Are downgrading activities logged and auditable?',
        },
        {
            'type': 'downgrading_restrictions',
            'question': 'What restrictions exist on data downgrading (approval requirements, prohibited downgrades, retention requirements)? Are restrictions enforced?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-8 compliance? Provide: Data downgrading procedures, approval records, tag change logs, access control updates. Where are these artifacts stored?',
        },
    ],
    
    # Program Management (PM)
    'pm-1': [
        {
            'type': 'security_program',
            'question': 'Do you have a documented information security program for AWS? Does it include governance, risk management, compliance, and continuous improvement?',
        },
        {
            'type': 'program_leadership',
            'question': 'Who leads the AWS security program (CISO, security director, cloud security lead)? Do they have appropriate authority and resources?',
        },
        {
            'type': 'program_review',
            'question': 'How often is the security program reviewed and updated (annually, after major changes, continuous improvement)? Are metrics tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-1 compliance? Provide: Security program documentation, program charter, leadership appointments, program review records. Where are these artifacts stored?',
        },
    ],
    'pm-2': [
        {
            'type': 'senior_leadership',
            'question': 'How is senior leadership involved in AWS security (security briefings, risk acceptance decisions, budget approval, policy approval)? How often do they review security?',
        },
        {
            'type': 'security_reporting',
            'question': 'What security metrics are reported to leadership (Security Hub findings, compliance status, incident trends, risk posture)? How frequently?',
        },
        {
            'type': 'leadership_decisions',
            'question': 'What security decisions require leadership approval (risk acceptance, major security investments, policy exceptions, incident response escalation)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-2 compliance? Provide: Leadership security briefing materials, meeting minutes, security metrics reports, leadership decision records. Where are these artifacts stored?',
        },
    ],
    'pm-3': [
        {
            'type': 'security_resources',
            'question': 'What resources are allocated to AWS security (security tools budget, security staff, training budget, incident response resources)? Are resources adequate?',
        },
        {
            'type': 'resource_planning',
            'question': 'How are security resource needs identified and planned (risk assessments, security roadmap, capacity planning)? Who approves resource allocation?',
        },
        {
            'type': 'resource_tracking',
            'question': 'How are security resources tracked (budget tracking, staff utilization, tool usage)? Are resources used effectively?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-3 compliance? Provide: Security budget documentation, staffing plans, resource allocation decisions, resource utilization reports. Where are these artifacts stored?',
        },
    ],
    'pm-4': [
        {
            'type': 'action_plans',
            'question': 'Do you have action plans for AWS security improvements (POA&M, security roadmap, remediation plans)? Are plans tracked and updated?',
        },
        {
            'type': 'plan_tracking',
            'question': 'How are action plans tracked (project management tools, POA&M tracking, Security Hub custom actions)? Are milestones monitored?',
        },
        {
            'type': 'plan_reporting',
            'question': 'How often are action plan status updates provided to management (weekly, monthly, quarterly)? Are delays escalated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-4 compliance? Provide: Security action plans, POA&M status reports, milestone tracking, management status updates. Where are these artifacts stored?',
        },
    ],
    'pm-5': [
        {
            'type': 'system_inventory',
            'question': 'Do you maintain an inventory of AWS systems and services (accounts, regions, services used, data classification)? How is inventory maintained?',
        },
        {
            'type': 'inventory_automation',
            'question': 'Is inventory automated (AWS Config, Systems Manager Inventory, third-party CMDB, tagging)? How often is inventory updated?',
        },
        {
            'type': 'inventory_accuracy',
            'question': 'How is inventory accuracy verified (automated discovery, periodic reviews, reconciliation)? Are discrepancies investigated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-5 compliance? Provide: AWS system inventory, Config resource inventory, inventory update procedures, accuracy verification records. Where are these artifacts stored?',
        },
    ],
    'pm-6': [
        {
            'type': 'security_measures',
            'question': 'What security measures are implemented in AWS (encryption, access controls, monitoring, logging, incident response, vulnerability management)? Are measures documented?',
        },
        {
            'type': 'measure_effectiveness',
            'question': 'How is security measure effectiveness assessed (metrics, testing, audits, penetration tests)? Are ineffective measures improved or replaced?',
        },
        {
            'type': 'measure_review',
            'question': 'How often are security measures reviewed (annually, after incidents, continuous improvement)? Who conducts reviews?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-6 compliance? Provide: Security measures documentation, effectiveness assessment reports, measure review records, improvement plans. Where are these artifacts stored?',
        },
    ],
    'pm-7': [
        {
            'type': 'insider_threat',
            'question': 'Do you have an insider threat program for AWS (user behavior monitoring, privileged access monitoring, data exfiltration detection)? What tools support this?',
        },
        {
            'type': 'threat_detection',
            'question': 'How are insider threats detected (GuardDuty, CloudTrail anomaly detection, Macie for data access, third-party UEBA)? Are alerts investigated?',
        },
        {
            'type': 'threat_response',
            'question': 'What is your response to suspected insider threats (investigation procedures, access suspension, forensics, legal involvement)? Who leads investigations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-7 compliance? Provide: Insider threat program documentation, detection tool configurations, investigation procedures, incident records (redacted). Where are these artifacts stored?',
        },
    ],
    'pm-8': [
        {
            'type': 'critical_infrastructure',
            'question': 'Have you identified critical AWS infrastructure (production accounts, critical services, data stores, authentication systems)? Is criticality documented?',
        },
        {
            'type': 'protection_measures',
            'question': 'What additional protections exist for critical infrastructure (enhanced monitoring, stricter access controls, redundancy, backup)? Are protections tested?',
        },
        {
            'type': 'criticality_review',
            'question': 'How often is infrastructure criticality reassessed (annually, after architecture changes, after incidents)? Who approves criticality designations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-8 compliance? Provide: Critical infrastructure inventory, protection measures documentation, criticality assessment records. Where are these artifacts stored?',
        },
    ],
    'pm-9': [
        {
            'type': 'risk_strategy',
            'question': 'What is your AWS risk management strategy (risk identification, assessment, mitigation, acceptance, monitoring)? Is it documented and approved?',
        },
        {
            'type': 'risk_assessment',
            'question': 'How often are AWS risks assessed (continuously, quarterly, annually, after major changes)? What methodology is used?',
        },
        {
            'type': 'risk_acceptance',
            'question': 'What is your risk acceptance process (risk register, acceptance criteria, approval authority, time limits)? Are accepted risks reviewed periodically?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-9 compliance? Provide: Risk management strategy document, risk assessment reports, risk register, risk acceptance documentation. Where are these artifacts stored?',
        },
    ],
    'pm-10': [
        {
            'type': 'security_authorization',
            'question': 'What is your AWS security authorization strategy (continuous ATO, traditional ATO, risk-based authorization)? Is it documented?',
        },
        {
            'type': 'authorization_scope',
            'question': 'What is the scope of authorization (per account, per workload, entire AWS environment)? How are authorization boundaries defined?',
        },
        {
            'type': 'reauthorization',
            'question': 'How often is reauthorization required (every 3 years, after major changes, continuous authorization)? What triggers reauthorization?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-10 compliance? Provide: Authorization strategy document, authorization boundaries, authorization decision letters, reauthorization schedule. Where are these artifacts stored?',
        },
    ],
    'pm-11': [
        {
            'type': 'mission_functions',
            'question': 'Have you identified mission-critical functions supported by AWS (customer-facing applications, financial systems, operational systems)? Is criticality documented?',
        },
        {
            'type': 'function_protection',
            'question': 'What protections exist for mission-critical functions (high availability, disaster recovery, enhanced monitoring, incident response priority)? Are protections tested?',
        },
        {
            'type': 'function_review',
            'question': 'How often are mission-critical functions reassessed (annually, after business changes, after incidents)? Who approves criticality designations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-11 compliance? Provide: Mission-critical functions inventory, protection measures documentation, criticality assessment records. Where are these artifacts stored?',
        },
    ],
    'pm-12': [
        {
            'type': 'insider_threat_program',
            'question': 'Do you have a comprehensive insider threat program for AWS (detection, prevention, response, deterrence)? Is it documented and resourced?',
        },
        {
            'type': 'program_components',
            'question': 'What components does your insider threat program include (user monitoring, privileged access management, data loss prevention, security awareness, incident response)?',
        },
        {
            'type': 'program_effectiveness',
            'question': 'How is insider threat program effectiveness measured (incidents detected, response time, false positive rate, user awareness)? Are metrics reviewed?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-12 compliance? Provide: Insider threat program documentation, program metrics, detection tool configurations, incident response records (redacted). Where are these artifacts stored?',
        },
    ],
    'pm-13': [
        {
            'type': 'security_workforce',
            'question': 'Do you have adequate AWS security workforce (security engineers, architects, analysts, incident responders)? Are roles clearly defined?',
        },
        {
            'type': 'workforce_development',
            'question': 'How is the security workforce developed (AWS certifications, security training, conferences, hands-on labs)? Is training budget adequate?',
        },
        {
            'type': 'workforce_retention',
            'question': 'What is your strategy for retaining security talent (competitive compensation, career development, challenging work, work-life balance)? What is turnover rate?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-13 compliance? Provide: Security workforce plan, role definitions, training records, certification records, retention metrics. Where are these artifacts stored?',
        },
    ],
    'pm-14': [
        {
            'type': 'testing_program',
            'question': 'Do you have a security testing program for AWS (vulnerability scanning, penetration testing, red team exercises, security assessments)? How often is testing conducted?',
        },
        {
            'type': 'testing_scope',
            'question': 'What is tested (applications, infrastructure, IAM policies, network configurations, incident response procedures)? Are all critical systems tested?',
        },
        {
            'type': 'testing_remediation',
            'question': 'How are testing findings remediated (POA&M tracking, SLA-based remediation, verification testing)? Are findings tracked to closure?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-14 compliance? Provide: Security testing program documentation, testing schedule, test reports, remediation tracking, retest results. Where are these artifacts stored?',
        },
    ],
    'pm-15': [
        {
            'type': 'contacts',
            'question': 'Have you designated security contacts for AWS (security team email, incident response hotline, AWS account alternate contacts)? Are contacts documented and current?',
        },
        {
            'type': 'contact_availability',
            'question': 'Are security contacts available 24/7 for critical incidents? Is there an escalation path for after-hours incidents?',
        },
        {
            'type': 'contact_communication',
            'question': 'How are security contacts communicated (employee handbook, intranet, security awareness training, AWS account settings)? Are contacts tested periodically?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-15 compliance? Provide: Security contacts documentation, AWS account contact settings, contact communication records, contact test results. Where are these artifacts stored?',
        },
    ],
    'pm-16': [
        {
            'type': 'threat_awareness',
            'question': 'How do you stay aware of AWS security threats (AWS Security Bulletins, GuardDuty findings, threat intelligence feeds, security communities)? Who monitors threats?',
        },
        {
            'type': 'threat_sharing',
            'question': 'Do you share threat information (industry ISACs, AWS security forums, peer organizations)? Do you receive threat intelligence from external sources?',
        },
        {
            'type': 'threat_response',
            'question': 'How are new threats addressed (security advisories, emergency patches, configuration changes, monitoring updates)? What is the response timeline?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-16 compliance? Provide: Threat intelligence sources documentation, threat monitoring reports, threat response records, information sharing agreements. Where are these artifacts stored?',
        },
    ],
    
    # PII Processing and Transparency (PT)
    'pt-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented policies for PII processing in AWS (collection, use, retention, disclosure, disposal)? Does it comply with privacy regulations (GDPR, CCPA)?',
        },
        {
            'type': 'aws_pii_protection',
            'question': 'Does your policy address AWS-specific PII protection (encryption, access controls, data residency, Macie for PII discovery, data lifecycle management)?',
        },
        {
            'type': 'privacy_compliance',
            'question': 'What privacy regulations apply to your AWS PII (GDPR, CCPA, HIPAA, FERPA)? How do you ensure compliance? Are Data Processing Agreements in place with AWS?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-1 compliance? Provide: PII processing policy document with approval signatures, privacy compliance documentation, AWS DPA, policy review records. Where are these artifacts stored?',
        },
    ],
    'pt-2': [
        {
            'type': 'authority_to_collect',
            'question': 'What is your legal authority to collect PII in AWS (consent, contract, legitimate interest, legal obligation)? Is authority documented for each PII type?',
        },
        {
            'type': 'collection_limitation',
            'question': 'Do you limit PII collection to what is necessary (data minimization)? How is necessity determined? Are collection practices reviewed?',
        },
        {
            'type': 'consent_management',
            'question': 'If using consent, how is it obtained and managed (consent forms, consent management platform, audit trail)? Can consent be withdrawn?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-2 compliance? Provide: Legal authority documentation, data minimization assessments, consent records, collection limitation policies. Where are these artifacts stored?',
        },
    ],
    'pt-3': [
        {
            'type': 'pii_inventory',
            'question': 'Do you maintain an inventory of PII in AWS (data types, locations, purposes, retention periods)? How is inventory maintained?',
        },
        {
            'type': 'pii_discovery',
            'question': 'How do you discover PII in AWS (Macie for S3, database scanning, application inventory, data flow mapping)? Is discovery automated?',
        },
        {
            'type': 'inventory_accuracy',
            'question': 'How is PII inventory accuracy verified (periodic reviews, automated discovery, data classification validation)? Are discrepancies investigated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-3 compliance? Provide: PII inventory, Macie discovery reports, data flow diagrams, inventory update procedures. Where are these artifacts stored?',
        },
    ],
    'pt-4': [
        {
            'type': 'consent_management',
            'question': 'How do you manage consent for PII processing in AWS (consent capture, consent storage, consent withdrawal, consent audit trail)? Is consent granular?',
        },
        {
            'type': 'consent_verification',
            'question': 'How do you verify consent before processing PII (consent checks in applications, consent database, automated verification)? Are consent violations prevented?',
        },
        {
            'type': 'consent_withdrawal',
            'question': 'How can individuals withdraw consent? What happens to their PII after withdrawal (deletion, anonymization, processing cessation)? Is withdrawal honored promptly?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-4 compliance? Provide: Consent management procedures, consent records, withdrawal requests and responses, consent verification logs. Where are these artifacts stored?',
        },
    ],
    'pt-5': [
        {
            'type': 'privacy_notice',
            'question': 'Do you provide privacy notices for PII collection in AWS (what PII, why collected, how used, who has access, retention period, rights)? Are notices clear and accessible?',
        },
        {
            'type': 'notice_timing',
            'question': 'When are privacy notices provided (at collection, before processing, in privacy policy)? Are notices provided in multiple languages if needed?',
        },
        {
            'type': 'notice_updates',
            'question': 'How are privacy notices updated when practices change? Are individuals notified of material changes? How is notification documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-5 compliance? Provide: Privacy notices, notice delivery records, notice update history, user acknowledgment records. Where are these artifacts stored?',
        },
    ],
    'pt-6': [
        {
            'type': 'data_subject_rights',
            'question': 'How do individuals exercise privacy rights for AWS PII (access, correction, deletion, portability, objection)? Is there a request process?',
        },
        {
            'type': 'request_handling',
            'question': 'What is your process for handling privacy rights requests (request verification, data retrieval, response timeline, appeal process)? Are requests tracked?',
        },
        {
            'type': 'response_timeline',
            'question': 'What are your response timelines for privacy rights requests (30 days for GDPR, 45 days for CCPA)? Are timelines met? Are delays communicated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-6 compliance? Provide: Privacy rights request procedures, request tracking records, response documentation, timeline compliance reports. Where are these artifacts stored?',
        },
    ],
    'pt-7': [
        {
            'type': 'pii_redress',
            'question': 'How can individuals seek redress for PII issues (complaints, disputes, corrections)? Is there a complaint process? Who handles complaints?',
        },
        {
            'type': 'complaint_handling',
            'question': 'What is your complaint handling process (complaint receipt, investigation, resolution, response, appeal)? Are complaints tracked and analyzed?',
        },
        {
            'type': 'redress_timeline',
            'question': 'What are your timelines for complaint resolution? Are individuals kept informed of progress? Is there an escalation path?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-7 compliance? Provide: Complaint handling procedures, complaint records (redacted), resolution documentation, timeline compliance reports. Where are these artifacts stored?',
        },
    ],
    'pt-8': [
        {
            'type': 'computer_matching',
            'question': 'Do you perform computer matching of PII in AWS (data matching, record linkage, data analytics)? Is matching authorized and documented?',
        },
        {
            'type': 'matching_agreements',
            'question': 'If performing computer matching, do you have matching agreements (purpose, data sources, matching criteria, retention, oversight)? Are agreements reviewed?',
        },
        {
            'type': 'matching_safeguards',
            'question': 'What safeguards protect PII during matching (access controls, encryption, audit logging, data minimization, accuracy verification)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-8 compliance? Provide: Computer matching agreements, matching procedures, safeguard documentation, matching audit logs. Where are these artifacts stored?',
        },
    ],
    
    # Supply Chain Risk Management (SR)
    'sr-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented supply chain risk management policies for AWS (vendor assessment, third-party risk, software supply chain, service provider oversight)? When was it last reviewed?',
        },
        {
            'type': 'aws_supply_chain',
            'question': 'Does your policy address AWS-specific supply chain risks (third-party integrations, marketplace solutions, open source dependencies, container images, Lambda layers)?',
        },
        {
            'type': 'risk_assessment',
            'question': 'How do you assess supply chain risks (vendor security assessments, dependency scanning, third-party audits, continuous monitoring)? How often?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-1 compliance? Provide: Supply chain risk management policy document with approval signatures, risk assessment procedures, policy review records. Where are these artifacts stored?',
        },
    ],
    'sr-2': [
        {
            'type': 'supplier_reviews',
            'question': 'How often do you review AWS service providers and third-party vendors (annually, after security incidents, continuous monitoring)? What is reviewed?',
        },
        {
            'type': 'review_criteria',
            'question': 'What criteria are used in supplier reviews (security posture, compliance certifications, incident history, financial stability, contract compliance)?',
        },
        {
            'type': 'review_actions',
            'question': 'What actions result from supplier reviews (continued use, enhanced monitoring, contract renegotiation, supplier termination)? Who approves actions?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-2 compliance? Provide: Supplier review schedule, review reports, review criteria documentation, action records. Where are these artifacts stored?',
        },
    ],
    'sr-3': [
        {
            'type': 'supply_chain_controls',
            'question': 'What supply chain security controls are required for AWS vendors (security assessments, SOC 2 reports, penetration testing, incident response capabilities)?',
        },
        {
            'type': 'control_verification',
            'question': 'How do you verify vendor security controls (audit reports, security questionnaires, on-site assessments, continuous monitoring)? How often?',
        },
        {
            'type': 'control_deficiencies',
            'question': 'How are vendor control deficiencies addressed (remediation plans, compensating controls, contract enforcement, vendor termination)? Are deficiencies tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-3 compliance? Provide: Vendor security requirements, SOC 2 reports, security assessment results, deficiency remediation records. Where are these artifacts stored?',
        },
    ],
    'sr-4': [
        {
            'type': 'provenance',
            'question': 'How do you verify the provenance of AWS components (container images from trusted registries, signed AMIs, verified Lambda layers, authenticated packages)?',
        },
        {
            'type': 'integrity_verification',
            'question': 'How do you verify component integrity (checksum verification, digital signatures, ECR image scanning, artifact signing)? Is verification automated?',
        },
        {
            'type': 'unauthorized_components',
            'question': 'How are unauthorized or unverified components detected and prevented (admission controllers, Config rules, automated scanning)? Are violations blocked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-4 compliance? Provide: Provenance verification procedures, integrity verification logs, ECR scanning reports, unauthorized component alerts. Where are these artifacts stored?',
        },
    ],
    'sr-5': [
        {
            'type': 'acquisition_strategies',
            'question': 'What strategies reduce supply chain risk in AWS acquisitions (multiple vendors, trusted sources, security requirements in contracts, vendor diversity)?',
        },
        {
            'type': 'vendor_diversity',
            'question': 'Do you avoid single points of failure in your AWS supply chain (multiple cloud providers, multiple SaaS vendors, alternative solutions)? Is diversity documented?',
        },
        {
            'type': 'risk_mitigation',
            'question': 'What mitigations address supply chain risks (vendor monitoring, contract terms, insurance, incident response plans, alternative vendors)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-5 compliance? Provide: Acquisition strategy documentation, vendor diversity analysis, risk mitigation plans, contract security terms. Where are these artifacts stored?',
        },
    ],
    'sr-6': [
        {
            'type': 'tamper_resistance',
            'question': 'How do you protect AWS components from tampering (code signing, artifact repositories with access controls, immutable infrastructure, integrity monitoring)?',
        },
        {
            'type': 'tamper_detection',
            'question': 'How is tampering detected (file integrity monitoring, CloudTrail for unauthorized changes, Config for drift detection, GuardDuty for malicious activity)?',
        },
        {
            'type': 'tamper_response',
            'question': 'What is your response to detected tampering (incident response, forensics, component replacement, root cause analysis)? Are incidents tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-6 compliance? Provide: Tamper protection mechanisms, integrity monitoring configurations, tamper detection alerts, incident response records. Where are these artifacts stored?',
        },
    ],
    'sr-7': [
        {
            'type': 'supply_chain_operations',
            'question': 'What operational security practices protect your AWS supply chain (secure development, secure deployment, access controls, monitoring, incident response)?',
        },
        {
            'type': 'operations_monitoring',
            'question': 'How are supply chain operations monitored (dependency updates, vendor security advisories, vulnerability disclosures, threat intelligence)? Who monitors?',
        },
        {
            'type': 'operations_response',
            'question': 'How do you respond to supply chain security events (vulnerability patches, vendor breaches, compromised dependencies)? What is the response timeline?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-7 compliance? Provide: Supply chain operations procedures, monitoring reports, security advisory tracking, incident response records. Where are these artifacts stored?',
        },
    ],
    'sr-8': [
        {
            'type': 'notification_agreements',
            'question': 'Do you have agreements with AWS vendors for security notification (breach notification, vulnerability disclosure, security advisories, incident reporting)?',
        },
        {
            'type': 'notification_timeline',
            'question': 'What are the notification timelines in vendor agreements (immediate for breaches, 24 hours for critical vulnerabilities, weekly for advisories)? Are timelines enforced?',
        },
        {
            'type': 'notification_response',
            'question': 'How do you respond to vendor security notifications (impact assessment, remediation, communication, incident response)? Are responses tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-8 compliance? Provide: Vendor notification agreements, notification records, response documentation, timeline compliance reports. Where are these artifacts stored?',
        },
    ],
    'sr-9': [
        {
            'type': 'tamper_evident',
            'question': 'How do you make AWS supply chain tampering evident (audit logging, integrity monitoring, version control, change tracking, digital signatures)?',
        },
        {
            'type': 'evidence_preservation',
            'question': 'How is tampering evidence preserved (log retention, immutable logs, forensic copies, chain of custody)? How long is evidence retained?',
        },
        {
            'type': 'evidence_review',
            'question': 'How often is tampering evidence reviewed (continuous monitoring, periodic audits, after incidents)? Who reviews evidence?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-9 compliance? Provide: Tamper-evident mechanisms, audit log configurations, evidence preservation procedures, review records. Where are these artifacts stored?',
        },
    ],
    'sr-10': [
        {
            'type': 'component_inspection',
            'question': 'How do you inspect AWS components for tampering (vulnerability scanning, malware scanning, code review, integrity verification, provenance checks)?',
        },
        {
            'type': 'inspection_frequency',
            'question': 'How often are components inspected (before deployment, continuously, after updates, randomly)? Is inspection automated?',
        },
        {
            'type': 'inspection_findings',
            'question': 'How are inspection findings handled (component rejection, remediation, investigation, vendor notification)? Are findings tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-10 compliance? Provide: Component inspection procedures, inspection reports, finding remediation records, automated scanning configurations. Where are these artifacts stored?',
        },
    ],
    'sr-11': [
        {
            'type': 'component_authenticity',
            'question': 'How do you verify AWS component authenticity (digital signatures, trusted sources, certificate validation, vendor verification)?',
        },
        {
            'type': 'authenticity_enforcement',
            'question': 'Is component authenticity verification enforced (automated checks, deployment gates, admission controllers)? Can unauthenticated components be deployed?',
        },
        {
            'type': 'authenticity_failures',
            'question': 'How are authenticity verification failures handled (deployment blocking, alerts, investigation, vendor contact)? Are failures tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-11 compliance? Provide: Authenticity verification procedures, verification logs, deployment gate configurations, failure records. Where are these artifacts stored?',
        },
    ],
    'sr-12': [
        {
            'type': 'component_disposal',
            'question': 'How do you dispose of AWS supply chain components (decommissioning procedures, data sanitization, license termination, vendor notification)?',
        },
        {
            'type': 'disposal_verification',
            'question': 'How is component disposal verified (deletion confirmation, data sanitization verification, license cancellation confirmation)? Is disposal documented?',
        },
        {
            'type': 'disposal_data_protection',
            'question': 'How is data protected during component disposal (encryption, sanitization, secure deletion, vendor data deletion requests)? Are data protection requirements met?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-12 compliance? Provide: Component disposal procedures, disposal verification records, data sanitization logs, vendor termination confirmations. Where are these artifacts stored?',
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

"""
Enrich MCP data with ControlCompass managed controls for NIST controls missing coverage.
Maps AWS Control Guides from ControlCompass to NIST SP 800-53 controls.
"""
import json

with open('backend/compliance_discovery/aws_controls_mcp_data.json') as f:
    data = json.load(f)

controls = data.get('controls', {})

total = len(controls)
has_managed = sum(1 for cid, entries in controls.items()
    if any(e.get('config_rules') or e.get('security_hub_controls') or e.get('control_tower_ids') for e in entries))
print(f"Before enrichment: {has_managed}/{total} controls have managed controls")


def entry(control_id, title, description, services, config_rules=None, security_hub_controls=None, control_tower_ids=None, frameworks=None):
    return {
        "control_id": control_id,
        "title": title,
        "description": description,
        "services": services,
        "config_rules": config_rules or [],
        "security_hub_controls": security_hub_controls or [],
        "control_tower_ids": control_tower_ids or [],
        "frameworks": frameworks or ["NIST-SP-800-53-r5"]
    }


enrichments = {
    # === AC Family (Access Control) ===

    # AC-7: Unsuccessful Logon Attempts
    "ac-7": [
        entry("AWS-CG-0000048", "Implement MFA for the AWS root account",
              "Enable MFA for the root account to reduce brute-force and unauthorized access risk.",
              ["AWS Identity and Access Management"],
              ["ROOT_ACCOUNT_MFA_ENABLED"], ["IAM.9"], ["AWS-GR_ROOT_ACCOUNT_MFA_ENABLED"]),
        entry("AWS-CG-0000139", "Enable hardware MFA for the root account",
              "Enable hardware MFA for the root account to protect against unauthorized access.",
              ["AWS Identity and Access Management"],
              ["ROOT_ACCOUNT_HARDWARE_MFA_ENABLED"], ["IAM.6"], ["SH.IAM.6"]),
        entry("AWS-CG-0000184", "Enforce account password policy for IAM users",
              "Define strong password parameters within the AWS account password policy.",
              ["AWS Identity and Access Management"],
              ["IAM_PASSWORD_POLICY"], ["IAM.10"], ["SH.IAM.7"]),
        entry("AWS-CG-0000138", "Enable MFA for IAM console users",
              "Enable MFA for IAM users with console passwords to strengthen authentication.",
              ["AWS Identity and Access Management"],
              ["MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"], ["IAM.5"], ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS", "SH.IAM.5"]),
    ],

    # AC-8: System Use Notification
    "ac-8": [
        entry("AWS-CG-0000263", "Restrict and monitor the use of AWS root account",
              "Restrict and monitor root user usage to support system use notification requirements.",
              ["AWS Identity and Access Management"],
              [], ["CloudWatch.1"], []),
    ],

    # AC-11: Session Lock
    "ac-11": [
        entry("AWS-CG-0000207", "Enable Amazon S3 bucket object lock",
              "Enable object lock in S3 buckets to protect against unintentional changes or deletions.",
              ["Amazon S3"],
              ["S3_BUCKET_DEFAULT_LOCK_ENABLED"], ["S3.15"], ["CONFIG.S3.DT.9"]),
        entry("AWS-CG-0000198", "Block public access to Amazon S3 buckets",
              "Configure S3 to block public access to protect data from unauthorized access.",
              ["Amazon S3"],
              ["S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS", "S3_BUCKET_PUBLIC_READ_PROHIBITED", "S3_BUCKET_PUBLIC_WRITE_PROHIBITED"],
              ["S3.1", "S3.2", "S3.3", "S3.8"],
              ["AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC", "CT.S3.PR.1", "SH.S3.1", "SH.S3.2"]),
    ],

    # AC-12: Session Termination
    "ac-12": [
        entry("AWS-CG-0000229", "Configure custom TLS policies for ELB listeners",
              "Configure custom TLS policies for ELB listeners to manage session security.",
              ["AWS Elastic Load Balancing"],
              ["ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"], ["ELB.3", "ELB.8"], ["SH.ELB.3", "SH.ELB.8"]),
        entry("AWS-CG-0000281", "Enable encryption for data in transit for DMS endpoints",
              "Enable encryption for DMS endpoints to prevent unauthorized access during data transfer.",
              ["AWS Database Migration Service"],
              ["DMS_ENDPOINT_SSL_CONFIGURED"], ["DMS.9"], ["SH.DMS.9"]),
    ],


    # === AU Family (Audit and Accountability) ===

    # AU-5: Response to Audit Logging Process Failures
    "au-5": [
        entry("AWS-CG-0000017", "Ensure CloudWatch alarms cannot be disabled",
              "Verify CloudWatch alarm actions are enabled to support audit failure alerting.",
              ["Amazon CloudWatch"],
              ["CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK"], ["CloudWatch.17"], []),
        entry("AWS-CG-0000018", "Verify CloudWatch alarm settings",
              "Verify CloudWatch alarm settings are properly configured for audit monitoring.",
              ["Amazon CloudWatch"],
              ["CLOUDWATCH_ALARM_SETTINGS_CHECK"], [], []),
        entry("AWS-CG-0000010", "Enable CloudTrail integration with CloudWatch Logs",
              "Send CloudTrail logs to CloudWatch for real-time audit failure monitoring and alerting.",
              ["AWS CloudTrail", "Amazon CloudWatch"],
              ["CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"], ["CloudTrail.5"], ["AWS-GR_CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"]),
    ],

    # AU-7: Audit Record Reduction and Report Generation
    "au-7": [
        entry("AWS-CG-0000244", "Configure CloudWatch log group retention period",
              "Set retention periods on CloudWatch log groups to support audit record management.",
              ["Amazon CloudWatch"],
              ["CW_LOGGROUP_RETENTION_PERIOD_CHECK"], ["CloudWatch.16"], []),
        entry("AWS-CG-0000201", "Enable Amazon S3 bucket logging",
              "Enable S3 bucket logging to support audit record collection and analysis.",
              ["Amazon S3"],
              ["S3_BUCKET_LOGGING_ENABLED"], ["S3.9"], ["CT.S3.PR.9"]),
    ],

    # AU-8: Time Stamps
    "au-8": [
        entry("AWS-CG-0000014", "Enable CloudTrail log file validation",
              "Enable log file validation to ensure integrity and timestamping of audit records.",
              ["AWS CloudTrail"],
              ["CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"], ["CloudTrail.4"], ["AWS-GR_CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"]),
        entry("AWS-CG-0000010", "Enable CloudTrail integration with CloudWatch Logs",
              "Integrate CloudTrail with CloudWatch for time-synchronized audit record processing.",
              ["AWS CloudTrail", "Amazon CloudWatch"],
              ["CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"], ["CloudTrail.5"], ["AWS-GR_CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"]),
    ],

    # === CA Family (Assessment, Authorization, and Monitoring) ===

    # CA-3: Information Exchange
    "ca-3": [
        entry("AWS-CG-0000229", "Configure custom TLS policies for ELB listeners",
              "Configure TLS policies for ELB to secure information exchange between systems.",
              ["AWS Elastic Load Balancing"],
              ["ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"], ["ELB.3", "ELB.8"], ["SH.ELB.3", "SH.ELB.8"]),
        entry("AWS-CG-0000066", "Enable VPC endpoint services",
              "Use VPC endpoints to secure information exchange within AWS without traversing the internet.",
              ["Amazon VPC"],
              ["SERVICE_VPC_ENDPOINT_ENABLED"], ["EC2.10"], []),
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to monitor and assess information exchange security posture.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
    ],

    # CA-9: Internal System Connections
    "ca-9": [
        entry("AWS-CG-0000062", "Enable VPC flow logs",
              "Enable VPC flow logs to monitor internal system connections and network traffic.",
              ["Amazon VPC"],
              ["VPC_FLOW_LOGS_ENABLED"], ["EC2.6"], ["AWS-GR_VPC_FLOW_LOGS_ENABLED"]),
        entry("AWS-CG-0000066", "Enable VPC endpoint services",
              "Use VPC endpoints to manage and secure internal system connections.",
              ["Amazon VPC"],
              ["SERVICE_VPC_ENDPOINT_ENABLED"], ["EC2.10"], []),
    ],

    # === CM Family (Configuration Management) ===

    # CM-5: Access Restrictions for Change
    "cm-5": [
        entry("AWS-CG-0000772", "Audit bucket policy changes prohibited",
              "Prevent unauthorized changes to audit bucket policies to maintain configuration integrity.",
              ["Amazon S3"],
              [], [], ["AWS-GR_AUDIT_BUCKET_POLICY_CHANGES_PROHIBITED"]),
        entry("AWS-CG-0000774", "Audit bucket retention policy",
              "Enforce retention policies on audit buckets to protect configuration change records.",
              ["Amazon S3"],
              [], [], ["AWS-GR_AUDIT_BUCKET_RETENTION_POLICY"]),
        entry("AWS-CG-0000046", "Restrict IAM policies with blacklisted actions",
              "Restrict IAM policies to prevent unauthorized configuration changes.",
              ["AWS Identity and Access Management"],
              ["IAM_POLICY_BLACKLISTED_CHECK"], ["IAM.2"], ["SH.IAM.2"]),
    ],

    # CM-9: Configuration Management Plan
    "cm-9": [
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to support configuration management monitoring.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
        entry("AWS-CG-0000046", "Restrict IAM policies with blacklisted actions",
              "Restrict IAM policies to enforce configuration management controls.",
              ["AWS Identity and Access Management"],
              ["IAM_POLICY_BLACKLISTED_CHECK"], ["IAM.2"], ["SH.IAM.2"]),
    ],

    # CM-10: Software Usage Restrictions
    "cm-10": [
        entry("AWS-CG-0000046", "Restrict IAM policies with blacklisted actions",
              "Restrict IAM policies to enforce software usage restrictions.",
              ["AWS Identity and Access Management"],
              ["IAM_POLICY_BLACKLISTED_CHECK"], ["IAM.2"], ["SH.IAM.2"]),
    ],

    # CM-11: User-Installed Software
    "cm-11": [
        entry("AWS-CG-0000046", "Restrict IAM policies with blacklisted actions",
              "Restrict IAM policies to control user-installed software.",
              ["AWS Identity and Access Management"],
              ["IAM_POLICY_BLACKLISTED_CHECK"], ["IAM.2"], ["SH.IAM.2"]),
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to detect unauthorized software installations.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
    ],

    # CM-12: Information Location
    "cm-12": [
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to track and monitor information location across AWS resources.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
    ],


    # === CP Family (Contingency Planning) ===

    # CP-3: Contingency Training
    "cp-3": [
        entry("AWS-CG-0000152", "Include EBS volumes in backup plans",
              "Include EBS volumes in AWS Backup plans to support contingency and recovery training.",
              ["Amazon EBS", "AWS Backup"],
              ["EBS_IN_BACKUP_PLAN"], ["EC2.28"], []),
        entry("AWS-CG-0000220", "Include EFS file systems in backup plans",
              "Include EFS file systems in AWS Backup plans for contingency preparedness.",
              ["Amazon EFS", "AWS Backup"],
              ["EFS_IN_BACKUP_PLAN"], ["EFS.2"], []),
        entry("AWS-CG-0000109", "Enforce backup recovery point minimum retention",
              "Enforce minimum retention for backup recovery points to support contingency operations.",
              ["AWS Backup"],
              ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"], [], []),
        entry("AWS-CG-0000275", "Encrypt backup recovery points",
              "Encrypt backup recovery points to protect contingency data.",
              ["AWS Backup"],
              ["BACKUP_RECOVERY_POINT_ENCRYPTED"], ["Backup.1"], []),
    ],

    # CP-8: Telecommunications Services
    "cp-8": [
        entry("AWS-CG-0000267", "Protect S3 resources with backup plans",
              "Protect S3 resources with backup plans for telecommunications service continuity.",
              ["Amazon S3", "AWS Backup"],
              ["S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN"], [], []),
        entry("AWS-CG-0000152", "Include EBS volumes in backup plans",
              "Include EBS volumes in backup plans for service continuity.",
              ["Amazon EBS", "AWS Backup"],
              ["EBS_IN_BACKUP_PLAN"], ["EC2.28"], []),
        entry("AWS-CG-0000109", "Enforce backup recovery point minimum retention",
              "Enforce minimum retention for recovery points to support service continuity.",
              ["AWS Backup"],
              ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"], [], []),
    ],

    # === IA Family (Identification and Authentication) ===

    # IA-3: Device Identification and Authentication
    "ia-3": [
        entry("AWS-CG-0000325", "Enable Network Firewall multi-AZ deployment",
              "Enable multi-AZ for Network Firewall to support device identification at network boundaries.",
              ["AWS Network Firewall"],
              ["NETFW_MULTI_AZ_ENABLED"], ["NetworkFirewall.1"], []),
        entry("AWS-CG-0000247", "Configure Network Firewall policies",
              "Configure Network Firewall policies to enforce device authentication requirements.",
              ["AWS Network Firewall"],
              [], ["NetworkFirewall.4"], []),
    ],

    # IA-6: Authentication Feedback
    "ia-6": [
        entry("AWS-CG-0000138", "Enable MFA for IAM console users",
              "Enable MFA for IAM console users to provide secure authentication feedback.",
              ["AWS Identity and Access Management"],
              ["MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"], ["IAM.5"], ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS", "SH.IAM.5"]),
        entry("AWS-CG-0000187", "Enable MFA for all IAM users",
              "Enable MFA for all IAM users to strengthen authentication mechanisms.",
              ["AWS Identity and Access Management"],
              ["IAM_USER_MFA_ENABLED"], ["IAM.19"], []),
    ],

    # IA-7: Cryptographic Module Authentication
    "ia-7": [
        entry("AWS-CG-0000033", "Enable EBS encryption by default",
              "Enable EBS encryption by default using validated cryptographic modules.",
              ["Amazon EBS", "AWS KMS"],
              ["EC2_EBS_ENCRYPTION_BY_DEFAULT"], ["EC2.7"], ["AWS-GR_EC2_EBS_ENCRYPTION_BY_DEFAULT", "SH.EC2.7"]),
        entry("AWS-CG-0000565", "Restrict KMS key policy public access",
              "Restrict KMS key policies to prevent public access to cryptographic modules.",
              ["AWS KMS"],
              ["KMS_KEY_POLICY_NO_PUBLIC_ACCESS"], [], []),
        entry("AWS-CG-0000275", "Encrypt backup recovery points",
              "Encrypt backup recovery points using validated cryptographic modules.",
              ["AWS Backup"],
              ["BACKUP_RECOVERY_POINT_ENCRYPTED"], ["Backup.1"], []),
    ],

    # IA-11: Re-authentication
    "ia-11": [
        entry("AWS-CG-0000138", "Enable MFA for IAM console users",
              "Enable MFA for IAM console users to support re-authentication requirements.",
              ["AWS Identity and Access Management"],
              ["MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"], ["IAM.5"], ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS", "SH.IAM.5"]),
        entry("AWS-CG-0000187", "Enable MFA for all IAM users",
              "Enable MFA for all IAM users to enforce re-authentication.",
              ["AWS Identity and Access Management"],
              ["IAM_USER_MFA_ENABLED"], ["IAM.19"], []),
    ],

    # IA-12: Identity Proofing
    "ia-12": [
        entry("AWS-CG-0000138", "Enable MFA for IAM console users",
              "Enable MFA for IAM console users to support identity proofing.",
              ["AWS Identity and Access Management"],
              ["MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"], ["IAM.5"], ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS", "SH.IAM.5"]),
        entry("AWS-CG-0000184", "Enforce account password policy for IAM users",
              "Enforce strong password policies to support identity proofing requirements.",
              ["AWS Identity and Access Management"],
              ["IAM_PASSWORD_POLICY"], ["IAM.10"], ["SH.IAM.7"]),
    ],


    # === IR Family (Incident Response) ===

    # IR-2: Incident Response Training
    "ir-2": [
        entry("AWS-CG-0000645", "Enable GuardDuty malware protection",
              "Enable GuardDuty malware protection to support incident response training scenarios.",
              ["Amazon GuardDuty"],
              ["GUARDDUTY_MALWARE_PROTECTION_ENABLED"], [], []),
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to provide incident data for response training.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
    ],

    # IR-3: Incident Response Testing
    "ir-3": [
        entry("AWS-CG-0000645", "Enable GuardDuty malware protection",
              "Enable GuardDuty malware protection to support incident response testing.",
              ["Amazon GuardDuty"],
              ["GUARDDUTY_MALWARE_PROTECTION_ENABLED"], [], []),
        entry("AWS-CG-0000275", "Encrypt backup recovery points",
              "Encrypt backup recovery points to support incident response and recovery testing.",
              ["AWS Backup"],
              ["BACKUP_RECOVERY_POINT_ENCRYPTED"], ["Backup.1"], []),
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to support incident response testing and validation.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
    ],

    # IR-7: Incident Response Assistance
    "ir-7": [
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to provide centralized incident response assistance.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
        entry("AWS-CG-0000645", "Enable GuardDuty malware protection",
              "Enable GuardDuty malware protection for automated incident detection assistance.",
              ["Amazon GuardDuty"],
              ["GUARDDUTY_MALWARE_PROTECTION_ENABLED"], [], []),
    ],

    # === SC Family (System and Communications Protection) ===

    # SC-2: Separation of User Functionality
    "sc-2": [
        entry("AWS-CG-0000338", "Ensure WAFv2 rule groups are not empty",
              "Ensure WAFv2 rule groups contain rules to separate user functionality from system management.",
              ["AWS WAF"],
              ["WAFV2_RULEGROUP_NOT_EMPTY"], [], []),
        entry("AWS-CG-0000374", "Configure WAF web ACL rules",
              "Configure WAF web ACLs to enforce separation of user and system functionality.",
              ["AWS WAF"],
              [], ["WAF.1"], []),
    ],

    # SC-4: Information in Shared Resources
    "sc-4": [
        entry("AWS-CG-0000063", "Close VPC default security groups",
              "Close VPC default security groups to prevent information leakage in shared resources.",
              ["Amazon VPC"],
              ["VPC_DEFAULT_SECURITY_GROUP_CLOSED"], ["EC2.2"], ["AWS-GR_VPC_DEFAULT_SECURITY_GROUP_CLOSED", "SH.EC2.2"]),
    ],

    # SC-10: Network Disconnect
    "sc-10": [
        entry("AWS-CG-0000229", "Configure custom TLS policies for ELB listeners",
              "Configure TLS policies for ELB to manage network session disconnection.",
              ["AWS Elastic Load Balancing"],
              ["ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"], ["ELB.3", "ELB.8"], ["SH.ELB.3", "SH.ELB.8"]),
        entry("AWS-CG-0000281", "Enable encryption for data in transit for DMS endpoints",
              "Enable DMS endpoint encryption to manage secure network disconnection.",
              ["AWS Database Migration Service"],
              ["DMS_ENDPOINT_SSL_CONFIGURED"], ["DMS.9"], ["SH.DMS.9"]),
    ],

    # SC-15: Collaborative Computing Devices and Applications
    "sc-15": [
        entry("AWS-CG-0000062", "Enable VPC flow logs",
              "Enable VPC flow logs to monitor collaborative computing device network traffic.",
              ["Amazon VPC"],
              ["VPC_FLOW_LOGS_ENABLED"], ["EC2.6"], ["AWS-GR_VPC_FLOW_LOGS_ENABLED"]),
        entry("AWS-CG-0000063", "Close VPC default security groups",
              "Close default security groups to restrict collaborative computing device access.",
              ["Amazon VPC"],
              ["VPC_DEFAULT_SECURITY_GROUP_CLOSED"], ["EC2.2"], ["AWS-GR_VPC_DEFAULT_SECURITY_GROUP_CLOSED", "SH.EC2.2"]),
    ],

    # SC-17: Public Key Infrastructure Certificates
    "sc-17": [
        entry("AWS-CG-0000733", "Check IAM server certificate expiration",
              "Monitor IAM server certificate expiration to maintain PKI certificate validity.",
              ["AWS Identity and Access Management"],
              ["IAM_SERVER_CERTIFICATE_EXPIRATION_CHECK"], [], []),
        entry("AWS-CG-0000333", "Disable ACM PCA root CA",
              "Disable ACM PCA root CA when not in use to protect PKI infrastructure.",
              ["AWS Certificate Manager"],
              ["ACM_PCA_ROOT_CA_DISABLED"], ["PCA.1"], []),
    ],

    # SC-18: Mobile Code
    "sc-18": [
        entry("AWS-CG-0000338", "Ensure WAFv2 rule groups are not empty",
              "Ensure WAFv2 rule groups contain rules to control mobile code execution.",
              ["AWS WAF"],
              ["WAFV2_RULEGROUP_NOT_EMPTY"], [], []),
        entry("AWS-CG-0000374", "Configure WAF web ACL rules",
              "Configure WAF web ACLs to filter and control mobile code.",
              ["AWS WAF"],
              [], ["WAF.1"], []),
    ],

    # SC-22: Architecture and Provisioning for Name/Address Resolution Service
    "sc-22": [
        entry("AWS-CG-0000325", "Enable Network Firewall multi-AZ deployment",
              "Enable multi-AZ Network Firewall to protect name resolution services.",
              ["AWS Network Firewall"],
              ["NETFW_MULTI_AZ_ENABLED"], ["NetworkFirewall.1"], []),
        entry("AWS-CG-0000062", "Enable VPC flow logs",
              "Enable VPC flow logs to monitor DNS and name resolution traffic.",
              ["Amazon VPC"],
              ["VPC_FLOW_LOGS_ENABLED"], ["EC2.6"], ["AWS-GR_VPC_FLOW_LOGS_ENABLED"]),
    ],

    # SC-23: Session Authenticity
    "sc-23": [
        entry("AWS-CG-0000229", "Configure custom TLS policies for ELB listeners",
              "Configure TLS policies for ELB to ensure session authenticity.",
              ["AWS Elastic Load Balancing"],
              ["ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"], ["ELB.3", "ELB.8"], ["SH.ELB.3", "SH.ELB.8"]),
        entry("AWS-CG-0000338", "Ensure WAFv2 rule groups are not empty",
              "Ensure WAFv2 rule groups contain rules to validate session authenticity.",
              ["AWS WAF"],
              ["WAFV2_RULEGROUP_NOT_EMPTY"], [], []),
    ],

    # SC-39: Process Isolation
    "sc-39": [
        entry("AWS-CG-0000063", "Close VPC default security groups",
              "Close default security groups to support process isolation between workloads.",
              ["Amazon VPC"],
              ["VPC_DEFAULT_SECURITY_GROUP_CLOSED"], ["EC2.2"], ["AWS-GR_VPC_DEFAULT_SECURITY_GROUP_CLOSED", "SH.EC2.2"]),
        entry("AWS-CG-0000066", "Enable VPC endpoint services",
              "Use VPC endpoints to isolate processes and limit network exposure.",
              ["Amazon VPC"],
              ["SERVICE_VPC_ENDPOINT_ENABLED"], ["EC2.10"], []),
    ],


    # === SI Family (System and Information Integrity) ===

    # SI-6: Security and Privacy Function Verification
    "si-6": [
        entry("AWS-CG-0000095", "Enable ECR private image scanning",
              "Enable ECR private image scanning to verify security function integrity.",
              ["Amazon ECR"],
              ["ECR_PRIVATE_IMAGE_SCANNING_ENABLED"], ["ECR.1"], []),
        entry("AWS-CG-0000696", "Enable Inspector ECR scanning",
              "Enable Inspector ECR scanning for automated security function verification.",
              ["Amazon Inspector"],
              ["INSPECTOR_ECR_SCAN_ENABLED"], [], []),
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to verify security function operation across AWS resources.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
    ],

    # SI-8: Spam Protection
    "si-8": [
        entry("AWS-CG-0000338", "Ensure WAFv2 rule groups are not empty",
              "Ensure WAFv2 rule groups contain rules to filter spam and malicious content.",
              ["AWS WAF"],
              ["WAFV2_RULEGROUP_NOT_EMPTY"], [], []),
        entry("AWS-CG-0000374", "Configure WAF web ACL rules",
              "Configure WAF web ACLs to protect against spam and unwanted traffic.",
              ["AWS WAF"],
              [], ["WAF.1"], []),
    ],

    # SI-10: Information Input Validation
    "si-10": [
        entry("AWS-CG-0000338", "Ensure WAFv2 rule groups are not empty",
              "Ensure WAFv2 rule groups contain rules for input validation.",
              ["AWS WAF"],
              ["WAFV2_RULEGROUP_NOT_EMPTY"], [], []),
        entry("AWS-CG-0000374", "Configure WAF web ACL rules",
              "Configure WAF web ACLs to validate and filter malicious input.",
              ["AWS WAF"],
              [], ["WAF.1"], []),
    ],

    # SI-11: Error Handling
    "si-11": [
        entry("AWS-CG-0000017", "Ensure CloudWatch alarms cannot be disabled",
              "Verify CloudWatch alarm actions are enabled to support error handling and alerting.",
              ["Amazon CloudWatch"],
              ["CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK"], ["CloudWatch.17"], []),
        entry("AWS-CG-0000010", "Enable CloudTrail integration with CloudWatch Logs",
              "Integrate CloudTrail with CloudWatch for error detection and handling.",
              ["AWS CloudTrail", "Amazon CloudWatch"],
              ["CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"], ["CloudTrail.5"], ["AWS-GR_CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"]),
    ],

    # SI-12: Information Management and Retention
    "si-12": [
        entry("AWS-CG-0000244", "Configure CloudWatch log group retention period",
              "Set retention periods on CloudWatch log groups for information management.",
              ["Amazon CloudWatch"],
              ["CW_LOGGROUP_RETENTION_PERIOD_CHECK"], ["CloudWatch.16"], []),
        entry("AWS-CG-0000267", "Protect S3 resources with backup plans",
              "Protect S3 resources with backup plans for information retention.",
              ["Amazon S3", "AWS Backup"],
              ["S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN"], [], []),
    ],

    # SI-16: Memory Protection
    "si-16": [
        entry("AWS-CG-0000095", "Enable ECR private image scanning",
              "Enable ECR image scanning to detect vulnerabilities that could affect memory protection.",
              ["Amazon ECR"],
              ["ECR_PRIVATE_IMAGE_SCANNING_ENABLED"], ["ECR.1"], []),
        entry("AWS-CG-0000568", "Enable Inspector Lambda standard scanning",
              "Enable Inspector Lambda scanning to detect memory protection vulnerabilities.",
              ["Amazon Inspector"],
              ["INSPECTOR_LAMBDA_STANDARD_SCAN_ENABLED"], [], []),
        entry("AWS-CG-0000645", "Enable GuardDuty malware protection",
              "Enable GuardDuty malware protection to detect memory-based threats.",
              ["Amazon GuardDuty"],
              ["GUARDDUTY_MALWARE_PROTECTION_ENABLED"], [], []),
    ],

    # === RA Family (Risk Assessment) ===

    # RA-7: Risk Response
    "ra-7": [
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to support risk response through centralized findings.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
        entry("AWS-CG-0000095", "Enable ECR private image scanning",
              "Enable ECR image scanning to identify risks requiring response.",
              ["Amazon ECR"],
              ["ECR_PRIVATE_IMAGE_SCANNING_ENABLED"], ["ECR.1"], []),
        entry("AWS-CG-0000696", "Enable Inspector ECR scanning",
              "Enable Inspector ECR scanning for automated risk identification.",
              ["Amazon Inspector"],
              ["INSPECTOR_ECR_SCAN_ENABLED"], [], []),
    ],

    # RA-9: Criticality Analysis
    "ra-9": [
        entry("AWS-CG-0000169", "Enable AWS Security Hub",
              "Enable Security Hub to support criticality analysis of AWS resources.",
              ["AWS Security Hub"],
              ["SECURITYHUB_ENABLED"], ["SecurityHub.1"], ["AWS-GR_SECURITYHUB_ENABLED"]),
        entry("AWS-CG-0000645", "Enable GuardDuty malware protection",
              "Enable GuardDuty malware protection to assess criticality of detected threats.",
              ["Amazon GuardDuty"],
              ["GUARDDUTY_MALWARE_PROTECTION_ENABLED"], [], []),
    ],
}

# === Apply enrichments ===
added_count = 0
enriched_controls = set()

for nist_id, new_entries in enrichments.items():
    if nist_id in controls:
        existing_cg_ids = {e.get('control_id') for e in controls[nist_id]}
        for new_entry in new_entries:
            if new_entry['control_id'] not in existing_cg_ids:
                controls[nist_id].append(new_entry)
                added_count += 1
                enriched_controls.add(nist_id)
    else:
        print(f"WARNING: NIST control '{nist_id}' not found in data, skipping")

print(f"\nEnriched {len(enriched_controls)} controls, added {added_count} new entries")

# Recount
has_managed_after = sum(1 for cid, entries in controls.items()
    if any(e.get('config_rules') or e.get('security_hub_controls') or e.get('control_tower_ids') for e in entries))
print(f"After enrichment: {has_managed_after}/{total} controls have managed controls ({has_managed_after*100//total}%)")
print(f"Improvement: +{has_managed_after - has_managed} controls")

# Save
data['controls'] = controls
with open('backend/compliance_discovery/aws_controls_mcp_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nSaved updated data to backend/compliance_discovery/aws_controls_mcp_data.json")

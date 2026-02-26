# Evidence questions for controls with AWS implementation data
# Add these to the respective control entries in CONTROL_QUESTIONS

# AC-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AC-1 compliance in AWS? Provide: Configuration screenshots from AWS Identity and Access Management, AWS Organizations; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AC-17
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AC-17 compliance in AWS? Provide: AWS Config compliance reports for EKS_ENDPOINT_NO_PUBLIC_ACCESS, S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS, S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC (and 4 more); Security Hub findings for EKS.1, S3.1, S3.2 (and 3 more); Control Tower compliance status for AWS-GR_EKS_ENDPOINT_NO_PUBLIC_ACCESS, SH.EKS.1 (and 10 more); Configuration screenshots from Amazon Elastic Kubernetes Service, Amazon S3, Amazon SageMaker; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AC-2
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AC-2 compliance in AWS? Provide: AWS Config compliance reports for MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, IAM_GROUP_HAS_USERS_CHECK, IAM_POLICY_IN_USE (and 1 more); Security Hub findings for IAM.5, IAM.18, IAM.19 (and 3 more); Control Tower compliance status for AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, SH.IAM.5 (and 5 more); Configuration screenshots from AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AC-3
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AC-3 compliance in AWS? Provide: AWS Config compliance reports for IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS, S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS, S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED (and 2 more); Security Hub findings for IAM.21, S3.1, S3.2 (and 3 more); Control Tower compliance status for SH.IAM.21, AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC (and 4 more); Configuration screenshots from AWS Identity and Access Management, Amazon Elastic Kubernetes Service, Amazon S3; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AC-6
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AC-6 compliance in AWS? Provide: AWS Config compliance reports for IAM_POLICY_IN_USE; Security Hub findings for IAM.18; Control Tower compliance status for CT.IAM.PR.1, CT.IAM.PR.5; Configuration screenshots from AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AU-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AU-1 compliance in AWS? Provide: AWS Config compliance reports for CLOUDTRAIL_SECURITY_TRAIL_ENABLED, CW_LOGGROUP_RETENTION_PERIOD_CHECK; Security Hub findings for CloudTrail.3, CloudWatch.16; Control Tower compliance status for CONFIG.CLOUDTRAIL.DT.6, CONFIG.LOGS.DT.2; Configuration screenshots from AWS CloudTrail, AWS Organizations, Amazon CloudWatch Logs (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AU-2
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AU-2 compliance in AWS? Provide: AWS Config compliance reports for MULTI_REGION_CLOUD_TRAIL_ENABLED, CLOUDTRAIL_SECURITY_TRAIL_ENABLED, CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED (and 2 more); Security Hub findings for CloudTrail.1, CloudTrail.3, CloudTrail.4 (and 2 more); Control Tower compliance status for SH.CloudTrail.1, CONFIG.CLOUDTRAIL.DT.6 (and 5 more); Configuration screenshots from AWS CloudTrail; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AU-3
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AU-3 compliance in AWS? Provide: AWS Config compliance reports for MULTI_REGION_CLOUD_TRAIL_ENABLED, CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED, CLOUDTRAIL_ALL_READ_S3_DATA_EVENT_CHECK; Security Hub findings for CloudTrail.1, CloudTrail.4; Control Tower compliance status for SH.CloudTrail.1, CT.CLOUDTRAIL.PR.2 (and 2 more); Configuration screenshots from AWS CloudTrail; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AU-6
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AU-6 compliance in AWS? Provide: AWS Config compliance reports for CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK, CW_LOGGROUP_RETENTION_PERIOD_CHECK, SECURITYHUB_ENABLED; Security Hub findings for CloudWatch.17, CloudWatch.16; Control Tower compliance status for CONFIG.CLOUDWATCH.DT.1, CONFIG.LOGS.DT.2 (and 1 more); Configuration screenshots from AWS Security Hub, Amazon CloudWatch, Amazon CloudWatch Logs; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# AU-9
{
    'type': 'evidence',
    'question': 'What evidence demonstrates AU-9 compliance in AWS? Provide: AWS Config compliance reports for S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED; Security Hub findings for CloudTrail.6, S3.8; Control Tower compliance status for AWS-GR_AUDIT_BUCKET_RETENTION_POLICY, AWS-GR_AUDIT_BUCKET_POLICY_CHANGES_PROHIBITED (and 2 more); Configuration screenshots from AWS CloudTrail, Amazon S3; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CM-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CM-1 compliance in AWS? Provide: AWS Config compliance reports for CLOUDFORMATION_STACK_NOTIFICATION_CHECK; Security Hub findings for CloudFormation.1; Control Tower compliance status for AWS-GR_CONFIG_ENABLED, CONFIG.CLOUDFORMATION.DT.1; Configuration screenshots from AWS CloudFormation, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CM-2
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CM-2 compliance in AWS? Provide: AWS Config compliance reports for EBS_IN_BACKUP_PLAN, EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN; Security Hub findings for EC2.28; Control Tower compliance status for AWS-GR_CONFIG_CHANGE_PROHIBITED, AWS-GR_CONFIG_RULE_CHANGE_PROHIBITED (and 2 more); Configuration screenshots from AWS Config, Amazon Elastic Block Store; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CM-3
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CM-3 compliance in AWS? Provide: AWS Config compliance reports for CLOUDFORMATION_STACK_NOTIFICATION_CHECK; Security Hub findings for CloudFormation.1; Control Tower compliance status for AWS-GR_CONFIG_CHANGE_PROHIBITED, CONFIG.CLOUDFORMATION.DT.1 (and 1 more); Configuration screenshots from AWS CloudFormation, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CM-7
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CM-7 compliance in AWS? Provide: AWS Config compliance reports for SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED, INCOMING_SSH_DISABLED, EC2_SECURITY_GROUP_ATTACHED_TO_ENI (and 1 more); Security Hub findings for EC2.15, EC2.13, EC2.22; Control Tower compliance status for AWS-GR_SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED, SH.EC2.15 (and 3 more); Configuration screenshots from Amazon EC2, Amazon VPC Lattice; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CM-8
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CM-8 compliance in AWS? Provide: Control Tower compliance status for CONFIG.APPCONFIG.DT.1, AWS-GR_CONFIG_CHANGE_PROHIBITED; Configuration screenshots from AWS AppConfig, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CP-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CP-1 compliance in AWS? Provide: AWS Config compliance reports for BACKUP_RECOVERY_POINT_ENCRYPTED, BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK; Security Hub findings for Backup.1; Control Tower compliance status for BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK; Configuration screenshots from AWS Backup, Amazon DynamoDB, Amazon RDS (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CP-2
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CP-2 compliance in AWS? Provide: AWS Config compliance reports for BACKUP_RECOVERY_POINT_ENCRYPTED, BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK, EFS_IN_BACKUP_PLAN (and 1 more); Security Hub findings for Backup.1, EFS.2; Control Tower compliance status for BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK, CONFIG.ELASTICFILESYSTEM.DT.4 (and 2 more); Configuration screenshots from AWS Backup, Amazon Elastic File System; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CP-4
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CP-4 compliance in AWS? Provide: AWS Config compliance reports for AURORA_LAST_BACKUP_RECOVERY_POINT_CREATED, VIRTUALMACHINE_LAST_BACKUP_RECOVERY_POINT_CREATED, BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED; Control Tower compliance status for AURORA_LAST_BACKUP_RECOVERY_POINT_CREATED, CONFIG.BACKUP-GATEWAY.DT.3 (and 1 more); Configuration screenshots from AWS Backup, Amazon RDS; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# CP-9
{
    'type': 'evidence',
    'question': 'What evidence demonstrates CP-9 compliance in AWS? Provide: AWS Config compliance reports for EBS_IN_BACKUP_PLAN, EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN, S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN (and 2 more); Security Hub findings for EC2.28, Backup.1; Control Tower compliance status for CONFIG.EC2.DT.14, CONFIG.EC2.DT.6 (and 3 more); Configuration screenshots from AWS Backup, Amazon Elastic Block Store, Amazon RDS (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# IA-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates IA-1 compliance in AWS? Provide: AWS Config compliance reports for IAM_PASSWORD_POLICY; Security Hub findings for IAM.7, IAM.8, IAM.9 (and 2 more); Control Tower compliance status for SH.IAM.7, SH.IAM.8; Configuration screenshots from AWS IAM Identity Center, AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# IA-2
{
    'type': 'evidence',
    'question': 'What evidence demonstrates IA-2 compliance in AWS? Provide: AWS Config compliance reports for MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, IAM_USER_MFA_ENABLED, ROOT_ACCOUNT_MFA_ENABLED; Security Hub findings for IAM.5, IAM.19, IAM.6; Control Tower compliance status for AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, SH.IAM.5 (and 3 more); Configuration screenshots from AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# IA-5
{
    'type': 'evidence',
    'question': 'What evidence demonstrates IA-5 compliance in AWS? Provide: AWS Config compliance reports for SECRETSMANAGER_SECRET_UNUSED, MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, IAM_USER_MFA_ENABLED; Security Hub findings for SecretsManager.3, IAM.5, IAM.19; Control Tower compliance status for SH.SecretsManager.3, AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS (and 2 more); Configuration screenshots from AWS Identity and Access Management, AWS Secrets Manager; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# IR-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates IR-1 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1; Configuration screenshots from AWS Security Hub, Amazon EventBridge; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# IR-4
{
    'type': 'evidence',
    'question': 'What evidence demonstrates IR-4 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED, GUARDDUTY_NON_ARCHIVED_FINDINGS, SECURITYHUB_ENABLED (and 1 more); Security Hub findings for GuardDuty.1, CloudWatch.17; Control Tower compliance status for CONFIG.GUARDDUTY.DT.1, SH.GuardDuty.1 (and 2 more); Configuration screenshots from AWS Security Hub, Amazon CloudWatch, Amazon GuardDuty; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# IR-8
{
    'type': 'evidence',
    'question': 'What evidence demonstrates IR-8 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED, CLOUDTRAIL_SECURITY_TRAIL_ENABLED, BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED; Security Hub findings for CloudTrail.3; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1, CONFIG.CLOUDTRAIL.DT.6 (and 1 more); Configuration screenshots from AWS Backup, AWS CloudTrail, AWS Security Hub; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# RA-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates RA-1 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1; Configuration screenshots from AWS Security Hub, AWS Trusted Advisor; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# RA-5
{
    'type': 'evidence',
    'question': 'What evidence demonstrates RA-5 compliance in AWS? Provide: AWS Config compliance reports for INSPECTOR_ENABLED, ECR_PRIVATE_IMAGE_SCANNING_ENABLED, EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK; Security Hub findings for ECR.1, SSM.2; Control Tower compliance status for SH.ECR.1, SH.SSM.2; Configuration screenshots from AWS Systems Manager, Amazon Elastic Container Registry, Amazon Inspector; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-1 compliance in AWS? Provide: AWS Config compliance reports for DYNAMODB_TABLE_ENCRYPTED_KMS, S3_DEFAULT_ENCRYPTION_KMS, RDS_STORAGE_ENCRYPTED; Security Hub findings for DynamoDB.1, S3.4, RDS.3; Control Tower compliance status for CONFIG.DYNAMODB.DT.4, SH.RDS.3; Configuration screenshots from AWS Config, AWS Key Management Service, AWS Organizations; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-12
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-12 compliance in AWS? Provide: AWS Config compliance reports for KMS_KEY_POLICY_NO_PUBLIC_ACCESS; Control Tower compliance status for CONFIG.KMS.DT.2, CT.KMS.PR.3 (and 1 more); Configuration screenshots from AWS Key Management Service; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-13
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-13 compliance in AWS? Provide: AWS Config compliance reports for DAX_TLS_ENDPOINT_ENCRYPTION, APPSYNC_CACHE_CT_ENCRYPTION_IN_TRANSIT, EMR_SECURITY_CONFIGURATION_ENCRYPTION_REST; Control Tower compliance status for CONFIG.DAX.DT.1, CONFIG.APPSYNC.DT.3 (and 1 more); Configuration screenshots from AWS AppSync, Amazon DynamoDB Accelerator (DAX), Amazon Elastic MapReduce; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-20
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-20 compliance in AWS? Provide: AWS Config compliance reports for ROUTE53_HOSTED_ZONE_TAGGED; Control Tower compliance status for CONFIG.ROUTE53.DT.2; Configuration screenshots from Amazon Route 53; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-21
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-21 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED; Security Hub findings for GuardDuty.1; Control Tower compliance status for SH.GuardDuty.1; Configuration screenshots from Amazon GuardDuty, Amazon Route 53; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-28
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-28 compliance in AWS? Provide: AWS Config compliance reports for DYNAMODB_TABLE_ENCRYPTED_KMS, KMS_KEY_POLICY_NO_PUBLIC_ACCESS, ELASTICSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK (and 2 more); Security Hub findings for ES.3, ES.8, Opensearch.3 (and 1 more); Control Tower compliance status for CONFIG.DYNAMODB.DT.4, CT.RDS.PR.16 (and 6 more); Configuration screenshots from AWS Key Management Service, Amazon DynamoDB, Amazon Kinesis Data Streams (and 2 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-7
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-7 compliance in AWS? Provide: AWS Config compliance reports for EC2_SECURITY_GROUP_ATTACHED_TO_ENI, EC2_SECURITY_GROUP_ATTACHED_TO_ENI_PERIODIC, VPC_DEFAULT_SECURITY_GROUP_CLOSED (and 6 more); Security Hub findings for EC2.22, EC2.2, NetworkFirewall.1 (and 3 more); Control Tower compliance status for CONFIG.EC2.DT.11, SH.EC2.22 (and 5 more); Configuration screenshots from AWS Elastic Load Balancing, AWS Network Firewall, Amazon EC2 (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SC-8
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SC-8 compliance in AWS? Provide: AWS Config compliance reports for ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK, ELB_PREDEFINED_SECURITY_POLICY_SSL_CHECK, ELB_TLS_HTTPS_LISTENERS_ONLY (and 4 more); Security Hub findings for ELB.3, ELB.8, ES.3 (and 3 more); Control Tower compliance status for SH.ELB.3, SH.ELB.8 (and 5 more); Configuration screenshots from AWS Elastic Load Balancing, Amazon OpenSearch Service; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SI-1
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SI-1 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED, INSPECTOR_ENABLED; Security Hub findings for GuardDuty.1; Control Tower compliance status for CONFIG.GUARDDUTY.DT.1, SH.GuardDuty.1; Configuration screenshots from AWS Security Hub, Amazon GuardDuty, Amazon Inspector; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SI-2
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SI-2 compliance in AWS? Provide: AWS Config compliance reports for EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK, RDS_AUTOMATIC_MINOR_VERSION_UPGRADE_ENABLED, LAMBDA_FUNCTION_SETTINGS_CHECK; Security Hub findings for SSM.2, RDS.13, Lambda.2; Control Tower compliance status for SH.SSM.2, SH.RDS.13 (and 1 more); Configuration screenshots from AWS Lambda, AWS Systems Manager, Amazon RDS; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SI-3
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SI-3 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_MALWARE_PROTECTION_ENABLED, GUARDDUTY_ENABLED_CENTRALIZED, GUARDDUTY_EKS_PROTECTION_AUDIT_ENABLED; Security Hub findings for GuardDuty.1; Control Tower compliance status for CONFIG.GUARDDUTY.DT.2, SH.GuardDuty.1 (and 1 more); Configuration screenshots from Amazon GuardDuty; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

# SI-4
{
    'type': 'evidence',
    'question': 'What evidence demonstrates SI-4 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_EKS_PROTECTION_RUNTIME_ENABLED, GUARDDUTY_NON_ARCHIVED_FINDINGS, GUARDDUTY_MALWARE_PROTECTION_ENABLED; Control Tower compliance status for CONFIG.GUARDDUTY.DT.7, CONFIG.GUARDDUTY.DT.1 (and 1 more); Configuration screenshots from Amazon GuardDuty; CloudTrail logs of relevant API calls. Where are these artifacts stored?',
},

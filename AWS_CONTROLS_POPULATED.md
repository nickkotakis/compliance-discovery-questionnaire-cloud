# AWS Implementation Guide - Controls Populated

## Summary

Successfully populated AWS control mappings for 6 key NIST 800-53 control families, covering 33 AWS-specific implementation controls.

## Controls Mapped

### 1. AC-2 (Account Management) - 10 AWS Controls
**Focus**: IAM user management, MFA, password policies

- **AWS-CG-0000138**: Enable MFA for IAM users with console password
  - Config Rule: `MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS`
  - Security Hub: IAM.5

- **AWS-CG-0000183**: Ensure all IAM user groups contain users
  - Config Rule: `IAM_GROUP_HAS_USERS_CHECK`

- **AWS-CG-0000185**: Manage access by creating and attaching IAM policies
  - Config Rule: `IAM_POLICY_IN_USE`
  - Security Hub: IAM.18

- **AWS-CG-0000187**: Configure MFA for IAM users
  - Config Rule: `IAM_USER_MFA_ENABLED`
  - Security Hub: IAM.19

- **AWS-CG-0000479**: Prevent IAM inline policies from using wildcard permissions
  - Control Tower: CT.IAM.PR.1

- **AWS-CG-0000574**: Enforce IAM password policy to require uppercase letter
  - Security Hub: IAM.11

- **AWS-CG-0000575**: Enforce strong password policies for IAM
  - Security Hub: IAM.7

- **AWS-CG-0000581**: Enforce IAM password policy to require lowercase letter
  - Security Hub: IAM.12

- **AWS-CG-0000760**: Ensure IAM users do not have policies directly attached
  - Control Tower: CT.IAM.PR.4

- **AWS-CG-0000761**: Restrict IAM inline policies from using wildcard service actions
  - Control Tower: CT.IAM.PR.5

### 2. AU-2 (Audit Events) - 5 AWS Controls
### 2. AU-2 (Audit Events) - 5 AWS Controls
**Focus**: CloudTrail logging and audit trail management

- **AWS-CG-0000008**: Configure AWS CloudTrail trails to be multi-region
  - Config Rule: `MULTI_REGION_CLOUD_TRAIL_ENABLED`
  - Security Hub: CloudTrail.1

- **AWS-CG-0000009**: Enable security trails in AWS CloudTrail
  - Config Rule: `CLOUDTRAIL_SECURITY_TRAIL_ENABLED`
  - Security Hub: CloudTrail.3

- **AWS-CG-0000014**: Enable log file validation for AWS CloudTrail logs
  - Config Rule: `CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED`
  - Security Hub: CloudTrail.4

- **AWS-CG-0000010**: Configure AWS CloudTrail to send logs to Amazon CloudWatch Logs
  - Config Rule: `CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED`
  - Security Hub: CloudTrail.5

- **AWS-CG-0000013**: Enable encryption for AWS CloudTrail trails
  - Config Rule: `CLOUD_TRAIL_ENCRYPTION_ENABLED`
  - Security Hub: CloudTrail.2

### 3. SC-7 (Boundary Protection) - 5 AWS Controls
**Focus**: Security groups, network firewalls, and boundary protection

- **AWS-CG-0000155**: Remove unused Amazon EC2 security groups
  - Config Rules: `EC2_SECURITY_GROUP_ATTACHED_TO_ENI`, `EC2_SECURITY_GROUP_ATTACHED_TO_ENI_PERIODIC`
  - Security Hub: EC2.22

- **AWS-CG-0000063**: Do not use default security group rules in Amazon VPC
  - Config Rule: `VPC_DEFAULT_SECURITY_GROUP_CLOSED`
  - Security Hub: EC2.2

- **AWS-CG-0000325**: Deploy AWS Network Firewalls across multiple Availability Zones
  - Config Rule: `NETFW_MULTI_AZ_ENABLED`
  - Security Hub: NetworkFirewall.1

- **AWS-CG-0000247**: Define default action for handling stateless packets in Network Firewall
  - Config Rules: `NETFW_POLICY_DEFAULT_ACTION_FRAGMENT_PACKETS`, `NETFW_POLICY_DEFAULT_ACTION_FULL_PACKETS`
  - Security Hub: NetworkFirewall.4

- **AWS-CG-0000229**: Configure custom TLS policies for Elastic Load Balancers
  - Config Rules: `ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK`, `ELB_PREDEFINED_SECURITY_POLICY_SSL_CHECK`, `ELB_TLS_HTTPS_LISTENERS_ONLY`
  - Security Hub: ELB.3, ELB.8

### 4. CP-9 (Backup) - 5 AWS Controls
**Focus**: AWS Backup, EBS, RDS, and S3 backup strategies

- **AWS-CG-0000152**: Backup Amazon EBS volumes
  - Config Rules: `EBS_IN_BACKUP_PLAN`, `EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN`
  - Security Hub: EC2.28

- **AWS-CG-0000379**: Ensure RDS instances have automatic backups (7+ days retention)
  - Control Tower: CT.RDS.PR.8

- **AWS-CG-0000267**: Configure AWS Backup Plan for Amazon S3 resources
  - Config Rule: `S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN`

- **AWS-CG-0000275**: Enable encryption at rest for AWS Backup recovery points
  - Config Rule: `BACKUP_RECOVERY_POINT_ENCRYPTED`
  - Security Hub: Backup.1

- **AWS-CG-0000109**: Configure recovery points to not expire before retention period
  - Config Rule: `BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK`

### 5. SC-28 (Data at Rest Protection) - 5 AWS Controls
**Focus**: Encryption using AWS KMS and service-specific encryption

- **AWS-CG-0000103**: Encrypt DynamoDB data at rest using AWS KMS
  - Config Rule: `DYNAMODB_TABLE_ENCRYPTED_KMS`

- **AWS-CG-0000587**: Ensure RDS database clusters have encryption at rest
  - Control Tower: CT.RDS.PR.16

- **AWS-CG-0000762**: Ensure Kinesis data streams have encryption at rest
  - Control Tower: CT.KINESIS.PR.1

- **AWS-CG-0000565**: Prevent public access in AWS KMS key policies
  - Config Rule: `KMS_KEY_POLICY_NO_PUBLIC_ACCESS`

- **AWS-CG-0000233**: Encrypt Amazon OpenSearch Service node communications
  - Config Rules: `ELASTICSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK`, `OPENSEARCH_HTTPS_REQUIRED`, `OPENSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK`
  - Security Hub: ES.3, ES.8, Opensearch.3, Opensearch.8

### 6. CM-2 (Baseline Configuration) - 3 AWS Controls
**Focus**: AWS Config and configuration management

- **AWS-CG-0000466**: Prevent unauthorized changes to AWS Config settings
  - Control Tower: AWS-GR_CONFIG_CHANGE_PROHIBITED

- **AWS-CG-0000465**: Prevent unauthorized modifications to AWS Config Rules
  - Control Tower: AWS-GR_CONFIG_RULE_CHANGE_PROHIBITED

- **AWS-CG-0000152**: Backup Amazon EBS volumes (also in CP-9)
  - Config Rules: `EBS_IN_BACKUP_PLAN`, `EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN`
  - Security Hub: EC2.28

## Coverage Statistics

- **Total NIST Controls Mapped**: 6
- **Total AWS Controls**: 33
- **AWS Services Covered**: 15+
  - AWS CloudTrail
  - Amazon EC2
  - Amazon VPC
  - AWS Network Firewall
  - AWS Elastic Load Balancing
  - Amazon EBS
  - Amazon RDS
  - Amazon S3
  - AWS Backup
  - Amazon DynamoDB
  - Amazon Kinesis
  - AWS KMS
  - Amazon OpenSearch
  - AWS Config
  - And more...

## Framework Alignment

All controls are aligned with:
- NIST SP 800-53 Rev 5
- PCI-DSS v4.0
- SOC 2 (SSAE-18)
- ISO/IEC 27001:2013

## How It Works

1. **Backend Loading**: The API server loads `aws_controls_mcp_data.json` on startup
2. **API Response**: When a control is requested, the API includes an `aws_controls` array
3. **Frontend Display**: The `AWSImplementationGuide` component renders the controls organized by AWS service
4. **User Experience**: Consultants see specific, actionable AWS guidance for each NIST control

## Next Steps

To add more controls:

1. Query the MCP server for additional NIST controls
2. Update `populate_aws_controls.py` with new control data
3. Run the script to regenerate `aws_controls_mcp_data.json`
4. Restart the backend server

Example controls to add next:
- IA-2 (Identification & Authentication)
- SI-2 (Flaw Remediation)
- SI-4 (System Monitoring)
- AC-3 (Access Enforcement)
- AC-17 (Remote Access)

## Files Modified

1. `backend/compliance_discovery/aws_controls_mcp_data.json` - AWS control mappings
2. `backend/populate_aws_controls.py` - Script to generate control mappings
3. `backend/compliance_discovery/api_server.py` - Already configured to load MCP data
4. `frontend/src/components/AWSImplementationGuide.tsx` - Already displays AWS controls
5. `frontend/src/components/ComplianceQuestionnaire.tsx` - Already integrated

## Testing

The backend server is now running with the new data:
```
Loaded MCP data for 6 controls from aws_controls_mcp_data.json
```

Open the frontend and navigate to any of these controls to see the AWS Implementation Guide:
- **AC-2** (Account Management) - 10 AWS controls
- **AU-2** (Audit Events) - 5 AWS controls
- **SC-7** (Boundary Protection) - 5 AWS controls
- **CP-9** (Backup) - 5 AWS controls
- **SC-28** (Data at Rest Protection) - 5 AWS controls
- **CM-2** (Baseline Configuration) - 3 AWS controls

# Adding More AWS Controls to MCP Data

## Current Status
✅ **AC-2** (Account Management): 10 AWS controls loaded and working

## Quick Win: Add Top 5 Most Common Controls

To demonstrate the AWS Implementation Guide across multiple control families, I recommend adding these 5 controls next:

### 1. AU-2 (Audit Events) - CloudTrail
**Search Query**: "CloudTrail logging audit events"
**Expected Results**: 15+ AWS controls
**Key Services**: AWS CloudTrail, CloudWatch Logs
**Key Config Rules**: 
- MULTI_REGION_CLOUD_TRAIL_ENABLED
- CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED
- CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED

### 2. SC-7 (Boundary Protection) - Security Groups
**Search Query**: "security groups boundary protection network"
**Expected Results**: 10+ AWS controls
**Key Services**: Amazon EC2, AWS Network Firewall, Security Groups
**Key Config Rules**:
- EC2_SECURITY_GROUP_ATTACHED_TO_ENI
- NETFW_MULTI_AZ_ENABLED

### 3. IA-2 (Identification & Authentication) - MFA
**Search Query**: "IAM authentication MFA"
**Expected Results**: 5+ AWS controls (overlap with AC-2)
**Key Services**: AWS IAM
**Key Config Rules**:
- MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS
- IAM_USER_MFA_ENABLED

### 4. CM-2 (Baseline Configuration) - AWS Config
**Search Query**: "Config baseline configuration"
**Expected Results**: 8+ AWS controls
**Key Services**: AWS Config, Systems Manager
**Key Config Rules**:
- CONFIG_ENABLED
- EC2_INSTANCE_MANAGED_BY_SSM

### 5. CP-9 (Backup) - AWS Backup
**Search Query**: "backup EBS RDS S3"
**Expected Results**: 10+ AWS controls
**Key Services**: AWS Backup, EBS, RDS, S3
**Key Config Rules**:
- BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK
- RDS_AUTOMATIC_MINOR_VERSION_UPGRADE_ENABLED

## Implementation Approach

Since manually querying and formatting each control is time-intensive, here are your options:

### Option A: Manual Addition (Recommended for Now)
I can query MCP for 2-3 more controls and add them to the JSON file. This gives you:
- AC-2 ✅ (Account Management)
- AU-2 (Audit Events)
- SC-7 (Boundary Protection)

This demonstrates the feature across 3 different control families.

### Option B: Bulk Export Script
Create a Python script that:
1. Reads all 177 controls from the NIST parser
2. Queries MCP for each using the keyword mapping
3. Generates comprehensive JSON file
4. Run time: ~10-15 minutes

### Option C: Incremental Addition
Add controls as consultants need them:
- Start with AC-2 (done)
- Add more when consultants click on other controls
- Build up the database organically

## My Recommendation

Let me add **AU-2** and **SC-7** right now to show the feature working across multiple control families. This will give you:

1. **Access Control** (AC-2) - IAM controls
2. **Audit & Accountability** (AU-2) - CloudTrail controls  
3. **System & Communications Protection** (SC-7) - Network controls

This demonstrates the breadth of AWS coverage and shows consultants the value immediately.

Would you like me to proceed with adding AU-2 and SC-7?

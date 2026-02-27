#!/usr/bin/env python3
"""
Add AWS Config rules, Security Hub controls, and Control Tower rules to customer responsibility controls
"""

import json

# Comprehensive mapping of NIST controls to AWS managed controls
AWS_MANAGED_CONTROLS = {
    # Access Control (AC)
    "ac-2": {
        "config_rules": ["IAM_USER_MFA_ENABLED", "IAM_GROUP_HAS_USERS_CHECK", "IAM_POLICY_IN_USE"],
        "security_hub_controls": ["IAM.5", "IAM.18", "IAM.19"],
        "control_tower_ids": ["CT.IAM.PR.1", "AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"]
    },
    "ac-3": {
        "config_rules": ["IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS", "IAM_USER_NO_POLICIES_CHECK"],
        "security_hub_controls": ["IAM.1", "IAM.2", "IAM.21"],
        "control_tower_ids": ["CT.IAM.PR.2", "CT.IAM.PR.3"]
    },
    "ac-4": {
        "config_rules": ["VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS", "VPC_DEFAULT_SECURITY_GROUP_CLOSED"],
        "security_hub_controls": ["EC2.2", "EC2.21", "EC2.22"],
        "control_tower_ids": ["CT.EC2.PR.1", "CT.EC2.PR.2"]
    },
    "ac-5": {
        "config_rules": ["IAM_ROOT_ACCESS_KEY_CHECK", "IAM_USER_UNUSED_CREDENTIALS_CHECK"],
        "security_hub_controls": ["IAM.4", "IAM.22"],
        "control_tower_ids": ["CT.IAM.PR.4"]
    },
    "ac-6": {
        "config_rules": ["IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS", "IAM_USER_NO_POLICIES_CHECK"],
        "security_hub_controls": ["IAM.1", "IAM.2"],
        "control_tower_ids": ["CT.IAM.PR.5"]
    },
    "ac-17": {
        "config_rules": ["EC2_INSTANCE_NO_PUBLIC_IP", "LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED"],
        "security_hub_controls": ["EC2.9", "Lambda.1"],
        "control_tower_ids": ["CT.EC2.PR.14", "CT.LAMBDA.PR.1"]
    },
    
    # Awareness and Training (AT)
    "at-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "at-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "at-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Audit and Accountability (AU)
    "au-2": {
        "config_rules": ["CLOUD_TRAIL_ENABLED", "CLOUDWATCH_LOG_GROUP_ENCRYPTED"],
        "security_hub_controls": ["CloudTrail.1", "CloudTrail.2", "CloudWatch.1"],
        "control_tower_ids": ["CT.CLOUDTRAIL.PR.1", "CT.CLOUDWATCH.PR.1"]
    },
    "au-3": {
        "config_rules": ["CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"],
        "security_hub_controls": ["CloudTrail.4"],
        "control_tower_ids": ["CT.CLOUDTRAIL.PR.2"]
    },
    "au-4": {
        "config_rules": ["CLOUDWATCH_ALARM_ACTION_CHECK"],
        "security_hub_controls": ["CloudWatch.2"],
        "control_tower_ids": []
    },
    "au-6": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": ["CT.GUARDDUTY.PR.1"]
    },
    "au-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "au-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "au-9": {
        "config_rules": ["CLOUD_TRAIL_ENCRYPTION_ENABLED", "S3_BUCKET_LOGGING_ENABLED"],
        "security_hub_controls": ["CloudTrail.2", "S3.9"],
        "control_tower_ids": ["CT.S3.PR.1"]
    },
    "au-11": {
        "config_rules": ["CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"],
        "security_hub_controls": ["CloudTrail.4"],
        "control_tower_ids": []
    },
    "au-12": {
        "config_rules": ["CLOUD_TRAIL_ENABLED", "VPC_FLOW_LOGS_ENABLED"],
        "security_hub_controls": ["CloudTrail.1", "EC2.6"],
        "control_tower_ids": ["CT.EC2.PR.3"]
    },
    
    # Security Assessment and Authorization (CA)
    "ca-2": {
        "config_rules": ["SECURITYHUB_ENABLED"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ca-7": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED", "SECURITYHUB_ENABLED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": []
    },
    "ca-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ca-9": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Configuration Management (CM)
    "cm-2": {
        "config_rules": ["APPROVED_AMIS_BY_TAG", "EC2_INSTANCE_MANAGED_BY_SSM"],
        "security_hub_controls": ["EC2.8", "SSM.1"],
        "control_tower_ids": ["CT.EC2.PR.4"]
    },
    "cm-3": {
        "config_rules": ["CLOUD_TRAIL_ENABLED"],
        "security_hub_controls": ["CloudTrail.1"],
        "control_tower_ids": []
    },
    "cm-4": {
        "config_rules": ["SECURITYHUB_ENABLED"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cm-6": {
        "config_rules": ["CONFIG_ENABLED"],
        "security_hub_controls": ["Config.1"],
        "control_tower_ids": ["CT.CONFIG.PR.1"]
    },
    "cm-7": {
        "config_rules": ["VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS", "EC2_INSTANCE_NO_PUBLIC_IP"],
        "security_hub_controls": ["EC2.2", "EC2.9"],
        "control_tower_ids": []
    },
    "cm-8": {
        "config_rules": ["REQUIRED_TAGS"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cm-10": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cm-11": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Contingency Planning (CP)
    "cp-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cp-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cp-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cp-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "cp-9": {
        "config_rules": ["DB_BACKUP_ENABLED", "DYNAMODB_PITR_ENABLED", "RDS_MULTI_AZ_SUPPORT"],
        "security_hub_controls": ["DynamoDB.2", "RDS.5"],
        "control_tower_ids": ["CT.RDS.PR.1"]
    },
    "cp-10": {
        "config_rules": ["DB_BACKUP_ENABLED"],
        "security_hub_controls": ["RDS.5"],
        "control_tower_ids": []
    },
    
    # Identification and Authentication (IA)
    "ia-2": {
        "config_rules": ["IAM_USER_MFA_ENABLED", "MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"],
        "security_hub_controls": ["IAM.5", "IAM.6"],
        "control_tower_ids": ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"]
    },
    "ia-4": {
        "config_rules": ["IAM_USER_NO_POLICIES_CHECK"],
        "security_hub_controls": ["IAM.2"],
        "control_tower_ids": []
    },
    "ia-5": {
        "config_rules": ["IAM_PASSWORD_POLICY", "SECRETSMANAGER_ROTATION_ENABLED_CHECK"],
        "security_hub_controls": ["IAM.7", "SecretsManager.1", "SecretsManager.2"],
        "control_tower_ids": ["CT.SECRETSMANAGER.PR.1"]
    },
    "ia-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ia-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Incident Response (IR)
    "ir-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ir-4": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": []
    },
    "ir-5": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ir-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ir-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ir-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Maintenance (MA)
    "ma-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ma-4": {
        "config_rules": ["EC2_INSTANCE_MANAGED_BY_SSM"],
        "security_hub_controls": ["SSM.1", "SSM.2"],
        "control_tower_ids": []
    },
    "ma-5": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Media Protection (MP)
    "mp-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "mp-5": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "mp-6": {
        "config_rules": ["S3_BUCKET_PUBLIC_READ_PROHIBITED", "S3_BUCKET_PUBLIC_WRITE_PROHIBITED"],
        "security_hub_controls": ["S3.1", "S3.2"],
        "control_tower_ids": ["CT.S3.PR.2"]
    },
    "mp-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Physical and Environmental Protection (PE)
    "pe-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-12": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-13": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-14": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-15": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pe-16": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Planning (PL)
    "pl-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pl-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pl-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Program Management (PM)
    "pm-1": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-5": {
        "config_rules": ["REQUIRED_TAGS"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-9": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-10": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-11": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-12": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-13": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-14": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-15": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pm-16": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Personnel Security (PS)
    "ps-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ps-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ps-5": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "ps-6": {
        "config_rules": ["IAM_USER_UNUSED_CREDENTIALS_CHECK"],
        "security_hub_controls": ["IAM.22"],
        "control_tower_ids": []
    },
    "ps-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # PII Processing and Transparency (PT)
    "pt-1": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-5": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-7": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "pt-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Risk Assessment (RA)
    "ra-3": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED", "SECURITYHUB_ENABLED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": []
    },
    "ra-5": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": []
    },
    
    # System and Services Acquisition (SA)
    "sa-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-4": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-5": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-9": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-10": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-11": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-15": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sa-22": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # System and Communications Protection (SC)
    "sc-5": {
        "config_rules": ["SHIELD_ADVANCED_ENABLED_AUTORENEW"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sc-7": {
        "config_rules": ["VPC_SG_OPEN_ONLY_TO_AUTHORIZED_PORTS", "VPC_DEFAULT_SECURITY_GROUP_CLOSED"],
        "security_hub_controls": ["EC2.2", "EC2.21"],
        "control_tower_ids": ["CT.EC2.PR.1"]
    },
    "sc-8": {
        "config_rules": ["ALB_HTTP_TO_HTTPS_REDIRECTION_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"],
        "security_hub_controls": ["ELB.1", "ELB.2"],
        "control_tower_ids": ["CT.ELB.PR.1"]
    },
    "sc-12": {
        "config_rules": ["KMS_CMK_NOT_SCHEDULED_FOR_DELETION"],
        "security_hub_controls": ["KMS.4"],
        "control_tower_ids": ["CT.KMS.PR.1"]
    },
    "sc-13": {
        "config_rules": ["S3_DEFAULT_ENCRYPTION_KMS", "RDS_STORAGE_ENCRYPTED"],
        "security_hub_controls": ["S3.4", "RDS.3"],
        "control_tower_ids": ["CT.S3.PR.3", "CT.RDS.PR.2"]
    },
    "sc-23": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sc-28": {
        "config_rules": ["ENCRYPTED_VOLUMES", "RDS_STORAGE_ENCRYPTED", "S3_DEFAULT_ENCRYPTION_KMS"],
        "security_hub_controls": ["EC2.7", "RDS.3", "S3.4"],
        "control_tower_ids": ["CT.EC2.PR.5", "CT.RDS.PR.2", "CT.S3.PR.3"]
    },
    
    # System and Information Integrity (SI)
    "si-2": {
        "config_rules": ["EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK"],
        "security_hub_controls": ["SSM.2"],
        "control_tower_ids": []
    },
    "si-3": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": []
    },
    "si-4": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED", "VPC_FLOW_LOGS_ENABLED"],
        "security_hub_controls": ["GuardDuty.1", "EC2.6"],
        "control_tower_ids": ["CT.EC2.PR.3"]
    },
    "si-5": {
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": []
    },
    "si-7": {
        "config_rules": ["CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"],
        "security_hub_controls": ["CloudTrail.4"],
        "control_tower_ids": []
    },
    "si-12": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "si-16": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    
    # Supply Chain Risk Management (SR)
    "sr-2": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sr-3": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sr-6": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sr-8": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "sr-11": {
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": []
    }
}

def add_managed_controls():
    """Add AWS managed controls to customer responsibility controls"""
    
    # Load the main MCP data file
    with open('backend/compliance_discovery/aws_controls_mcp_data.json', 'r') as f:
        data = json.load(f)
    
    controls_updated = 0
    
    # Iterate through all controls
    for control_id, control_list in data['controls'].items():
        if control_id in AWS_MANAGED_CONTROLS:
            managed_controls = AWS_MANAGED_CONTROLS[control_id]
            
            # Update each control in the list
            for control in control_list:
                # Only update if it's a customer responsibility control (has implementation_guidance)
                if 'implementation_guidance' in control:
                    control['config_rules'] = managed_controls['config_rules']
                    control['security_hub_controls'] = managed_controls['security_hub_controls']
                    control['control_tower_ids'] = managed_controls['control_tower_ids']
                    controls_updated += 1
                    print(f"Updated {control_id}: {control.get('title', 'N/A')}")
    
    # Save the updated data
    with open('backend/compliance_discovery/aws_controls_mcp_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Updated {controls_updated} customer responsibility controls with AWS managed controls")
    print(f"   - Config rules added")
    print(f"   - Security Hub controls added")
    print(f"   - Control Tower rules added")

if __name__ == '__main__':
    add_managed_controls()

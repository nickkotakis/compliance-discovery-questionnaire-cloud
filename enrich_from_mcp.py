#!/usr/bin/env python3
"""Enrich all controls in csf_aws_mappings.json with real MCP data.

For each control_id, update frameworks, config_rules, security_hub_controls,
and control_tower_ids with the verified MCP data. Also fix controls that
have wrong control_ids (e.g., AWS-CG-0000367 mapped as GuardDuty when
it's actually CloudTrail encryption).

Then re-classify priority tiers and sort.
"""

import json

# Real MCP data for all controls we looked up
# Format: control_id -> {title, description, services, frameworks, config_rules, security_hub, control_tower}
MCP_DATA = {
    "AWS-CG-0000180": {
        "title": "Enable Amazon GuardDuty in AWS account and region",
        "description": "Implement intrusion detection (IDS) capabilities by enabling GuardDuty in the AWS account and Region.",
        "services": ["Amazon GuardDuty"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"],
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": ["SH.GuardDuty.1"]
    },
    "AWS-CG-0000169": {
        "title": "Enable AWS Security Hub service",
        "description": "Activate Security Hub in the AWS management console and configure the service to receive findings from supported AWS security services.",
        "services": ["AWS Security Hub"],
        "frameworks": ["AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"],
        "config_rules": ["SECURITYHUB_ENABLED"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.SECURITYHUB.DT.1"]
    },
    "AWS-CG-0000077": {
        "title": "Encrypt backup recovery point in AWS Backup",
        "description": "Encrypt AWS Backup recovery point to protect information.",
        "services": ["AWS Backup"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"],
        "config_rules": ["BACKUP_RECOVERY_POINT_ENCRYPTED"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
    "AWS-CG-0000017": {
        "title": "Ensure Amazon CloudWatch alarms cannot be disabled",
        "description": "Ensure Amazon CloudWatch alarms cannot be disabled to allow continuous monitoring and timely responses.",
        "services": ["Amazon CloudWatch"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "CCCS-Medium-Cloud-Control-May-2019", "FedRAMP-r4", "NIST-SP-800-53-r5", "PCI-DSS-v4.0"],
        "config_rules": ["CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK"],
        "security_hub_controls": ["CloudWatch.17"],
        "control_tower_ids": ["CONFIG.CLOUDWATCH.DT.1"]
    },
    "AWS-CG-0000152": {
        "title": "Backup Amazon Elastic Block Storage (EBS) volumes",
        "description": "Configure automatic backups for Amazon EBS volumes to prevent data loss and support recovery.",
        "services": ["Amazon Elastic Block Store"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5"],
        "config_rules": ["EBS_IN_BACKUP_PLAN", "EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
        "security_hub_controls": ["EC2.28"],
        "control_tower_ids": ["CONFIG.EC2.DT.14", "CONFIG.EC2.DT.6"]
    },
    "AWS-CG-0000109": {
        "title": "Configure recovery points for AWS Backup with minimum retention",
        "description": "Configure recovery points for AWS Backup such that they do not expire before the retention period.",
        "services": ["AWS Backup"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "AWS-WAF-v10"],
        "config_rules": ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"],
        "security_hub_controls": [],
        "control_tower_ids": ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"]
    },
    "AWS-CG-0000220": {
        "title": "Enable a backup plan for Amazon Elastic File System (EFS)",
        "description": "Enable a backup plan for Amazon EFS to ensure that data is regularly backed up.",
        "services": ["Amazon Elastic File System"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "NIST-SP-800-53-r5"],
        "config_rules": ["EFS_IN_BACKUP_PLAN", "EFS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
        "security_hub_controls": ["EFS.2"],
        "control_tower_ids": ["CONFIG.ELASTICFILESYSTEM.DT.4", "CT.ELASTICFILESYSYSTEM.PR.2", "SH.EFS.2"]
    },
    "AWS-CG-0000095": {
        "title": "Enable private image repository scanning for Amazon ECR",
        "description": "Enable private image repository scanning for Amazon ECR to identify vulnerabilities in container images.",
        "services": ["Amazon Elastic Container Registry"],
        "frameworks": ["AWS-WAF-v10", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"],
        "config_rules": ["ECR_PRIVATE_IMAGE_SCANNING_ENABLED"],
        "security_hub_controls": ["ECR.1"],
        "control_tower_ids": ["CT.ECR.PR.2", "SH.ECR.1"]
    },
    "AWS-CG-0000080": {
        "title": "Send event notifications from CloudFormation stacks to SNS",
        "description": "Send event notifications from CloudFormation stacks to an SNS topic to notify personnel of potential security events.",
        "services": ["AWS CloudFormation"],
        "frameworks": ["AWS-WAF-v10", "NIST-SP-800-53-r5"],
        "config_rules": ["CLOUDFORMATION_STACK_NOTIFICATION_CHECK"],
        "security_hub_controls": ["CloudFormation.1"],
        "control_tower_ids": ["CONFIG.CLOUDFORMATION.DT.1"]
    },
    "AWS-CG-0000190": {
        "title": "Enable automatic minor version upgrades in Amazon RDS",
        "description": "Enable automatic minor version upgrades in Amazon RDS to update new features, bug fixes, and security patches.",
        "services": ["Amazon RDS"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"],
        "config_rules": ["RDS_AUTOMATIC_MINOR_VERSION_UPGRADE_ENABLED"],
        "security_hub_controls": ["RDS.13"],
        "control_tower_ids": ["CT.RDS.PR.5", "SH.RDS.13"]
    },
    "AWS-CG-0000094": {
        "title": "Patch Amazon EC2 instances",
        "description": "Patch EC2 instances in accordance with organization policies to remediate known vulnerabilities.",
        "services": ["Amazon EC2"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"],
        "config_rules": ["EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK"],
        "security_hub_controls": ["SSM.2"],
        "control_tower_ids": ["CONFIG.SSM.DT.1", "SH.SSM.2"]
    },
    "AWS-CG-0000143": {
        "title": "Configure AWS Lambda functions to use managed runtimes",
        "description": "Configure Lambda functions to use managed runtimes to benefit from automated updates and security enhancements.",
        "services": ["AWS Lambda"],
        "frameworks": ["PCI-DSS-v4.0"],
        "config_rules": ["LAMBDA_FUNCTION_SETTINGS_CHECK"],
        "security_hub_controls": ["Lambda.2"],
        "control_tower_ids": ["SH.Lambda.2"]
    },
    "AWS-CG-0000198": {
        "title": "Block public access to Amazon S3 buckets",
        "description": "Configure Amazon S3 to block public access to S3 buckets to protect data from unauthorized access.",
        "services": ["Amazon S3"],
        "frameworks": ["AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"],
        "config_rules": ["S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS", "S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC", "S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED", "S3_BUCKET_PUBLIC_READ_PROHIBITED", "S3_BUCKET_PUBLIC_WRITE_PROHIBITED"],
        "security_hub_controls": ["S3.1", "S3.2", "S3.3", "S3.8"],
        "control_tower_ids": ["AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC", "AWS-GR_S3_BUCKET_PUBLIC_READ_PROHIBITED", "AWS-GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED", "CONFIG.S3.DT.10", "CT.S3.PR.1", "SH.S3.1", "SH.S3.2", "SH.S3.3", "SH.S3.8"]
    },
    "AWS-CG-0000181": {
        "title": "Identify non-archived security findings in Amazon GuardDuty",
        "description": "Identify non-archived security findings in Amazon GuardDuty that exceed the configured number of days.",
        "services": ["Amazon GuardDuty"],
        "frameworks": ["NIST-SP-800-53-r5"],
        "config_rules": ["GUARDDUTY_NON_ARCHIVED_FINDINGS"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.GUARDDUTY.DT.1"]
    },
    "AWS-CG-0000267": {
        "title": "Configure AWS Backup Plan for Amazon S3 resources",
        "description": "Configure AWS Backup Plan for Amazon S3 resources to mitigate data loss and provide data protection.",
        "services": ["Amazon S3"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "NIST-SP-800-53-r5"],
        "config_rules": ["S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.S3.DT.3"]
    },
    "AWS-CG-0000229": {
        "title": "Configure custom TLS policies for listeners on AWS Elastic Load Balancers",
        "description": "Configure custom TLS policies for listeners on AWS ELB to customize security settings.",
        "services": ["AWS Elastic Load Balancing"],
        "frameworks": ["CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"],
        "config_rules": ["ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK", "ELB_PREDEFINED_SECURITY_POLICY_SSL_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"],
        "security_hub_controls": ["ELB.3", "ELB.8"],
        "control_tower_ids": ["SH.ELB.3", "SH.ELB.8"]
    },
    # Real data for AWS-CG-0000367 (CloudTrail encryption, NOT GuardDuty)
    "AWS-CG-0000367": {
        "title": "Ensure AWS CloudTrail trails have encryption at rest activated",
        "description": "Require CloudTrail trails to be configured with server-side encryption using AWS KMS-managed keys.",
        "services": ["AWS CloudTrail"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"],
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": ["CT.CLOUDTRAIL.PR.1"]
    },
    # Real data for AWS-CG-0000368 (CloudWatch log encryption, NOT SecurityHub)
    "AWS-CG-0000368": {
        "title": "Ensure CloudWatch log groups are encrypted at rest with AWS KMS keys",
        "description": "Enforce encryption of CloudWatch log groups at rest using AWS KMS customer-managed keys.",
        "services": ["Amazon CloudWatch"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"],
        "config_rules": [],
        "security_hub_controls": [],
        "control_tower_ids": ["CT.CLOUDWATCH.PR.3"]
    },
    # Real data for AWS-CG-0000696 (Inspector ECR scanning)
    "AWS-CG-0000696": {
        "title": "Enable ECR scanning in Amazon Inspector",
        "description": "Configure Amazon Inspector V2 ECR scanning to detect potential software vulnerabilities in container images.",
        "services": ["Amazon Inspector"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"],
        "config_rules": ["INSPECTOR_ECR_SCAN_ENABLED"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.INSPECTOR.DT.4"]
    },
    "AWS-CG-0000695": {
        "title": "Enable EKS runtime monitoring in Amazon GuardDuty",
        "description": "Enable GuardDuty EKS Runtime Monitoring to detect potential threats in EKS clusters.",
        "services": ["Amazon GuardDuty"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019"],
        "config_rules": ["GUARDDUTY_EKS_PROTECTION_RUNTIME_ENABLED"],
        "security_hub_controls": [],
        "control_tower_ids": []
    },
}

# Controls that were mapped with WRONG control_ids in the original enrichment.
# These need to be replaced with the correct control.
# Format: (wrong_id, wrong_config_rule) -> correct_control_id
WRONG_ID_FIXES = {
    # AWS-CG-0000367 is CloudTrail encryption, but was mapped as GuardDuty
    # The real GuardDuty control is AWS-CG-0000180
    ("AWS-CG-0000367", "GUARDDUTY_ENABLED_CENTRALIZED"): "AWS-CG-0000180",
    ("AWS-CG-0000367", "GUARDDUTY_NON_ARCHIVED_FINDINGS"): "AWS-CG-0000181",
    # AWS-CG-0000368 is CloudWatch encryption, but was mapped as SecurityHub
    ("AWS-CG-0000368", "SECURITYHUB_ENABLED"): "AWS-CG-0000169",
    # AWS-CG-0000369 was mapped as CloudWatch alarm check
    ("AWS-CG-0000369", "CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK"): "AWS-CG-0000017",
    # AWS-CG-0000370 was mapped as Inspector
    ("AWS-CG-0000370", "INSPECTOR_ENABLED"): None,  # No direct match, keep as-is but update metadata
    # AWS-CG-0000371 was mapped as ECR scanning
    ("AWS-CG-0000371", "ECR_PRIVATE_IMAGE_SCANNING_ENABLED"): "AWS-CG-0000095",
    # AWS-CG-0000372/373 were mapped as EC2 patch compliance
    ("AWS-CG-0000372", "EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK"): "AWS-CG-0000094",
    ("AWS-CG-0000373", "EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK"): "AWS-CG-0000094",
    # AWS-CG-0000374 was mapped as RDS auto minor version upgrade
    ("AWS-CG-0000374", "RDS_AUTOMATIC_MINOR_VERSION_UPGRADE_ENABLED"): "AWS-CG-0000190",
    # AWS-CG-0000375 was mapped as Lambda settings check
    ("AWS-CG-0000375", "LAMBDA_FUNCTION_SETTINGS_CHECK"): "AWS-CG-0000143",
}

# Core Config rules
CORE_CONFIG_RULES = {
    'S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED', 'S3_DEFAULT_ENCRYPTION_KMS',
    'ENCRYPTED_VOLUMES', 'EC2_EBS_ENCRYPTION_BY_DEFAULT',
    'RDS_STORAGE_ENCRYPTED', 'RDS_CLUSTER_ENCRYPTED_AT_REST',
    'DYNAMODB_TABLE_ENCRYPTED_KMS', 'CLOUDWATCH_LOG_GROUP_ENCRYPTED',
    'IAM_USER_MFA_ENABLED', 'MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS',
    'ROOT_ACCOUNT_MFA_ENABLED', 'IAM_ROOT_ACCESS_KEY_CHECK',
    'IAM_PASSWORD_POLICY', 'IAM_USER_UNUSED_CREDENTIALS_CHECK',
    'IAM_NO_INLINE_POLICY_CHECK', 'IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS',
    'IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS',
    'MULTI_REGION_CLOUD_TRAIL_ENABLED', 'CLOUDTRAIL_SECURITY_TRAIL_ENABLED',
    'CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED', 'VPC_FLOW_LOGS_ENABLED',
    'SECURITYHUB_ENABLED', 'GUARDDUTY_ENABLED_CENTRALIZED',
    'VPC_DEFAULT_SECURITY_GROUP_CLOSED', 'RESTRICTED_INCOMING_TRAFFIC',
    'S3_BUCKET_PUBLIC_READ_PROHIBITED', 'S3_BUCKET_PUBLIC_WRITE_PROHIBITED',
    'S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS', 'S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED',
    'RDS_INSTANCE_PUBLIC_ACCESS_CHECK',
    'S3_BUCKET_VERSIONING_ENABLED', 'S3_BUCKET_DEFAULT_LOCK_ENABLED',
    'BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK', 'DB_INSTANCE_BACKUP_ENABLED',
    'S3_BUCKET_REPLICATION_ENABLED', 'S3_BUCKET_SSL_REQUESTS_ONLY',
    'RDS_MULTI_AZ_SUPPORT', 'ELB_CROSS_ZONE_LOAD_BALANCING_ENABLED',
    'AUTOSCALING_GROUP_ELB_HEALTHCHECK_REQUIRED',
    'BACKUP_RECOVERY_POINT_ENCRYPTED',
    'EC2_MANAGEDINSTANCE_PATCH_COMPLIANCE_STATUS_CHECK',
    'ECR_PRIVATE_IMAGE_SCANNING_ENABLED',
    'CLOUDWATCH_ALARM_ACTION_ENABLED_CHECK',
    'ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK',
    'ELB_TLS_HTTPS_LISTENERS_ONLY',
}

MAJOR_FRAMEWORKS = {
    'CIS-AWS-Benchmark-v1.4', 'CIS-AWS-Benchmark-v1.3', 'CIS-AWS-Benchmark-v1.2',
    'CIS-v8.0', 'CIS-v7.1',
    'NIST-SP-800-53-r5', 'NIST-CSF-v1.1',
    'PCI-DSS-v4.0', 'PCI-DSS-v3.2.1',
    'SSAE-18-SOC-2-Oct-2023',
    'FedRAMP-r4',
    'ISO-IEC-27001:2013-Annex-A',
    'AWS-WAF-v10',
}


def classify_control(control):
    config_rules = set(control.get('config_rules', []))
    frameworks = set(control.get('frameworks', []))
    security_hub = control.get('security_hub_controls', [])
    control_tower = control.get('control_tower_ids', [])

    has_core_rule = bool(config_rules & CORE_CONFIG_RULES)
    major_count = len(frameworks & MAJOR_FRAMEWORKS)
    has_cis = any('CIS' in f for f in frameworks)
    has_security_hub = len(security_hub) > 0
    has_control_tower = len(control_tower) > 0

    # Synthetic controls (ID >= 785) are always enhanced
    cid_num = int(control['control_id'].replace('AWS-CG-', ''))
    if cid_num >= 785:
        return 'enhanced'

    # Core: fundamental controls
    if has_core_rule and major_count >= 4:
        return 'core'
    if has_core_rule and has_cis:
        return 'core'
    if has_security_hub and major_count >= 5:
        return 'core'
    if config_rules and major_count >= 6:
        return 'core'
    if has_cis and config_rules:
        return 'core'
    # Controls with Control Tower + many frameworks are important
    if has_control_tower and major_count >= 5:
        return 'core'

    # Recommended
    if config_rules and major_count >= 3:
        return 'recommended'
    if has_security_hub and major_count >= 2:
        return 'recommended'
    if config_rules and has_security_hub:
        return 'recommended'
    if has_control_tower and major_count >= 3:
        return 'recommended'
    if config_rules:
        return 'recommended'

    return 'enhanced'


def main():
    path = 'backend/compliance_discovery/csf_aws_mappings.json'
    with open(path) as f:
        data = json.load(f)

    # Step 1: Fix wrong control IDs
    fixes_applied = 0
    for key, controls in data['controls'].items():
        new_controls = []
        seen_ids = set()
        for c in controls:
            cid = c['control_id']
            first_rule = c.get('config_rules', [''])[0] if c.get('config_rules') else ''
            fix_key = (cid, first_rule)

            if fix_key in WRONG_ID_FIXES:
                new_id = WRONG_ID_FIXES[fix_key]
                if new_id and new_id not in seen_ids:
                    # Replace with correct control
                    mcp = MCP_DATA.get(new_id)
                    if mcp:
                        c['control_id'] = new_id
                        c['title'] = mcp['title']
                        c['description'] = mcp['description']
                        c['services'] = mcp['services']
                        c['frameworks'] = mcp['frameworks']
                        c['config_rules'] = mcp['config_rules']
                        c['security_hub_controls'] = mcp['security_hub_controls']
                        c['control_tower_ids'] = mcp['control_tower_ids']
                        fixes_applied += 1
                elif new_id is None:
                    # Keep as-is but don't duplicate
                    pass

            # Deduplicate
            if c['control_id'] not in seen_ids:
                seen_ids.add(c['control_id'])
                new_controls.append(c)

        data['controls'][key] = new_controls

    print(f'Fixed {fixes_applied} wrong control IDs')

    # Step 2: Enrich all controls with MCP data where available
    enriched = 0
    for key, controls in data['controls'].items():
        for c in controls:
            cid = c['control_id']
            if cid in MCP_DATA:
                mcp = MCP_DATA[cid]
                old_fw_count = len(c.get('frameworks', []))
                # Merge frameworks (union)
                c['frameworks'] = sorted(set(c.get('frameworks', [])) | set(mcp['frameworks']))
                # Merge managed controls (union)
                c['config_rules'] = sorted(set(c.get('config_rules', [])) | set(mcp['config_rules']))
                c['security_hub_controls'] = sorted(set(c.get('security_hub_controls', [])) | set(mcp['security_hub_controls']))
                c['control_tower_ids'] = sorted(set(c.get('control_tower_ids', [])) | set(mcp['control_tower_ids']))
                if len(c['frameworks']) != old_fw_count:
                    enriched += 1

    print(f'Enriched framework metadata for {enriched} control instances')

    # Step 3: Cross-pollinate - for each control_id, use richest metadata everywhere
    best_meta = {}
    for key, controls in data['controls'].items():
        for c in controls:
            cid = c['control_id']
            if cid not in best_meta:
                best_meta[cid] = {
                    'frameworks': set(c.get('frameworks', [])),
                    'config_rules': set(c.get('config_rules', [])),
                    'security_hub_controls': set(c.get('security_hub_controls', [])),
                    'control_tower_ids': set(c.get('control_tower_ids', [])),
                }
            else:
                best_meta[cid]['frameworks'] |= set(c.get('frameworks', []))
                best_meta[cid]['config_rules'] |= set(c.get('config_rules', []))
                best_meta[cid]['security_hub_controls'] |= set(c.get('security_hub_controls', []))
                best_meta[cid]['control_tower_ids'] |= set(c.get('control_tower_ids', []))

    normalized = 0
    for key, controls in data['controls'].items():
        for c in controls:
            cid = c['control_id']
            meta = best_meta[cid]
            old_fw = len(c.get('frameworks', []))
            c['frameworks'] = sorted(meta['frameworks'])
            c['config_rules'] = sorted(meta['config_rules'])
            c['security_hub_controls'] = sorted(meta['security_hub_controls'])
            c['control_tower_ids'] = sorted(meta['control_tower_ids'])
            if len(c['frameworks']) != old_fw:
                normalized += 1

    print(f'Cross-pollinated {normalized} additional control instances')

    # Step 4: Classify and sort
    stats = {'core': 0, 'recommended': 0, 'enhanced': 0}
    for key in sorted(data['controls'].keys()):
        controls = data['controls'][key]
        for c in controls:
            p = classify_control(c)
            c['priority'] = p
            stats[p] += 1
        data['controls'][key] = sorted(
            controls,
            key=lambda c: {'core': 0, 'recommended': 1, 'enhanced': 2}[c['priority']]
        )

    total = sum(stats.values())
    print(f'\nFinal classification ({total} total):')
    print(f'  Core:        {stats["core"]}')
    print(f'  Recommended: {stats["recommended"]}')
    print(f'  Enhanced:    {stats["enhanced"]}')

    # Show subcategory coverage
    with_core = 0
    without_core = 0
    total_subcats = 0
    for key, controls in sorted(data['controls'].items()):
        if len(controls) > 0:
            total_subcats += 1
            core_count = sum(1 for c in controls if c.get('priority') == 'core')
            if core_count > 0:
                with_core += 1
            else:
                without_core += 1
                if without_core <= 10:
                    print(f'  No core: {key} ({len(controls)} controls)')

    print(f'\nSubcategories with controls: {total_subcats}')
    print(f'  With core:    {with_core}')
    print(f'  Without core: {without_core}')

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'\nSaved to {path}')


if __name__ == '__main__':
    main()

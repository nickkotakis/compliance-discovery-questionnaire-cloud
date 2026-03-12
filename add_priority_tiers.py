#!/usr/bin/env python3
"""Add priority tiers to all AWS controls in csf_aws_mappings.json.

Tiers:
- "core": Fundamental controls for audit minimum. High framework coverage,
  broad applicability, Config rules present. These are the controls an
  organization should enable first.
- "recommended": Important controls that most organizations should implement.
  Good framework coverage but may be more service-specific.
- "enhanced": Niche or advanced controls for mature security programs.
  Service-specific, fewer framework mappings, or specialized use cases.

Classification logic:
1. Controls with 6+ framework mappings AND config rules = likely core
2. Controls appearing in CIS Benchmarks or multiple major frameworks = core
3. Controls with config rules but fewer frameworks = recommended
4. Controls without config rules or very niche services = enhanced
"""

import json

# Core Config rules that are fundamental for any AWS environment
CORE_CONFIG_RULES = {
    # Encryption fundamentals
    'S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED',
    'S3_DEFAULT_ENCRYPTION_KMS',
    'ENCRYPTED_VOLUMES',
    'EC2_EBS_ENCRYPTION_BY_DEFAULT',
    'RDS_STORAGE_ENCRYPTED',
    'RDS_CLUSTER_ENCRYPTED_AT_REST',
    'DYNAMODB_TABLE_ENCRYPTED_KMS',
    'CLOUDWATCH_LOG_GROUP_ENCRYPTED',
    # IAM fundamentals
    'IAM_USER_MFA_ENABLED',
    'MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS',
    'ROOT_ACCOUNT_MFA_ENABLED',
    'IAM_ROOT_ACCESS_KEY_CHECK',
    'IAM_PASSWORD_POLICY',
    'IAM_USER_UNUSED_CREDENTIALS_CHECK',
    'IAM_NO_INLINE_POLICY_CHECK',
    'IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS',
    'IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS',
    # Logging fundamentals
    'MULTI_REGION_CLOUD_TRAIL_ENABLED',
    'CLOUDTRAIL_SECURITY_TRAIL_ENABLED',
    'CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED',
    'VPC_FLOW_LOGS_ENABLED',
    'SECURITYHUB_ENABLED',
    'GUARDDUTY_ENABLED_CENTRALIZED',
    # Network fundamentals
    'VPC_DEFAULT_SECURITY_GROUP_CLOSED',
    'RESTRICTED_INCOMING_TRAFFIC',
    'S3_BUCKET_PUBLIC_READ_PROHIBITED',
    'S3_BUCKET_PUBLIC_WRITE_PROHIBITED',
    'S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS',
    'S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED',
    'RDS_INSTANCE_PUBLIC_ACCESS_CHECK',
    # Data protection fundamentals
    'S3_BUCKET_VERSIONING_ENABLED',
    'S3_BUCKET_DEFAULT_LOCK_ENABLED',
    'BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK',
    'DB_INSTANCE_BACKUP_ENABLED',
    'S3_BUCKET_REPLICATION_ENABLED',
    'S3_BUCKET_SSL_REQUESTS_ONLY',
    # Resilience fundamentals
    'RDS_MULTI_AZ_SUPPORT',
    'ELB_CROSS_ZONE_LOAD_BALANCING_ENABLED',
    'AUTOSCALING_GROUP_ELB_HEALTHCHECK_REQUIRED',
}

# Major frameworks that indicate broad applicability
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
    """Classify a control as core, recommended, or enhanced."""
    config_rules = set(control.get('config_rules', []))
    frameworks = set(control.get('frameworks', []))
    security_hub = control.get('security_hub_controls', [])
    control_tower = control.get('control_tower_ids', [])

    # Check if any config rule is in the core set
    has_core_rule = bool(config_rules & CORE_CONFIG_RULES)

    # Count major framework coverage
    major_count = len(frameworks & MAJOR_FRAMEWORKS)

    # Has CIS benchmark mapping (strong indicator of fundamental control)
    has_cis = any('CIS' in f for f in frameworks)

    # Has Security Hub control (indicates AWS considers it important)
    has_security_hub = len(security_hub) > 0

    # Synthetic controls (ID >= 785) are always enhanced
    cid_num = int(control['control_id'].replace('AWS-CG-', ''))
    if cid_num >= 785:
        return 'enhanced'

    # Core: fundamental controls
    if has_core_rule and major_count >= 4:
        return 'core'
    if has_core_rule and has_cis:
        return 'core'
    # High framework coverage with Security Hub = broadly important
    if has_security_hub and major_count >= 5:
        return 'core'
    # High framework coverage with config rules = broadly important
    if config_rules and major_count >= 6:
        return 'core'
    # CIS benchmark + config rules = fundamental
    if has_cis and config_rules:
        return 'core'

    # Recommended: good controls most orgs should have
    if config_rules and major_count >= 3:
        return 'recommended'
    if has_security_hub and major_count >= 2:
        return 'recommended'
    if config_rules and has_security_hub:
        return 'recommended'

    # Enhanced: everything else
    if config_rules:
        return 'recommended'

    return 'enhanced'


def main():
    mappings_path = 'backend/compliance_discovery/csf_aws_mappings.json'
    with open(mappings_path) as f:
        data = json.load(f)

    stats = {'core': 0, 'recommended': 0, 'enhanced': 0}
    total = 0

    for key in sorted(data['controls'].keys()):
        controls = data['controls'][key]
        for control in controls:
            priority = classify_control(control)
            control['priority'] = priority
            stats[priority] += 1
            total += 1

        # Sort controls: core first, then recommended, then enhanced
        data['controls'][key] = sorted(
            controls,
            key=lambda c: {'core': 0, 'recommended': 1, 'enhanced': 2}[c['priority']]
        )

    print(f'Total controls classified: {total}')
    print(f'  Core:        {stats["core"]}')
    print(f'  Recommended: {stats["recommended"]}')
    print(f'  Enhanced:    {stats["enhanced"]}')

    with open(mappings_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f'\nUpdated {mappings_path}')

    # Show a sample
    print('\n=== Sample: PR.DS-01 ===')
    for c in data['controls'].get('pr.ds-01', []):
        print(f'  [{c["priority"]:11s}] {c["control_id"]}: {c["title"][:60]}')


if __name__ == '__main__':
    main()

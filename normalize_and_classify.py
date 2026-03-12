#!/usr/bin/env python3
"""Normalize framework metadata across subcategories and re-classify priority tiers.

Problem: The same control_id (e.g., AWS-CG-0000169 SecurityHub) has different
framework counts depending on which subcategory it appears in, because different
enrichment scripts pulled different MCP data.

Fix: For each control_id, find the richest framework/config/securityhub/controltower
metadata and apply it everywhere that control appears.
"""

import json
from collections import defaultdict

# Core Config rules that are fundamental for any AWS environment
CORE_CONFIG_RULES = {
    'S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED',
    'S3_DEFAULT_ENCRYPTION_KMS',
    'ENCRYPTED_VOLUMES',
    'EC2_EBS_ENCRYPTION_BY_DEFAULT',
    'RDS_STORAGE_ENCRYPTED',
    'RDS_CLUSTER_ENCRYPTED_AT_REST',
    'DYNAMODB_TABLE_ENCRYPTED_KMS',
    'CLOUDWATCH_LOG_GROUP_ENCRYPTED',
    'IAM_USER_MFA_ENABLED',
    'MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS',
    'ROOT_ACCOUNT_MFA_ENABLED',
    'IAM_ROOT_ACCESS_KEY_CHECK',
    'IAM_PASSWORD_POLICY',
    'IAM_USER_UNUSED_CREDENTIALS_CHECK',
    'IAM_NO_INLINE_POLICY_CHECK',
    'IAM_POLICY_NO_STATEMENTS_WITH_ADMIN_ACCESS',
    'IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS',
    'MULTI_REGION_CLOUD_TRAIL_ENABLED',
    'CLOUDTRAIL_SECURITY_TRAIL_ENABLED',
    'CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED',
    'VPC_FLOW_LOGS_ENABLED',
    'SECURITYHUB_ENABLED',
    'GUARDDUTY_ENABLED_CENTRALIZED',
    'VPC_DEFAULT_SECURITY_GROUP_CLOSED',
    'RESTRICTED_INCOMING_TRAFFIC',
    'S3_BUCKET_PUBLIC_READ_PROHIBITED',
    'S3_BUCKET_PUBLIC_WRITE_PROHIBITED',
    'S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS',
    'S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED',
    'RDS_INSTANCE_PUBLIC_ACCESS_CHECK',
    'S3_BUCKET_VERSIONING_ENABLED',
    'S3_BUCKET_DEFAULT_LOCK_ENABLED',
    'BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK',
    'DB_INSTANCE_BACKUP_ENABLED',
    'S3_BUCKET_REPLICATION_ENABLED',
    'S3_BUCKET_SSL_REQUESTS_ONLY',
    'RDS_MULTI_AZ_SUPPORT',
    'ELB_CROSS_ZONE_LOAD_BALANCING_ENABLED',
    'AUTOSCALING_GROUP_ELB_HEALTHCHECK_REQUIRED',
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
    """Classify a control as core, recommended, or enhanced."""
    config_rules = set(control.get('config_rules', []))
    frameworks = set(control.get('frameworks', []))
    security_hub = control.get('security_hub_controls', [])

    has_core_rule = bool(config_rules & CORE_CONFIG_RULES)
    major_count = len(frameworks & MAJOR_FRAMEWORKS)
    has_cis = any('CIS' in f for f in frameworks)
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
    if has_security_hub and major_count >= 5:
        return 'core'
    if config_rules and major_count >= 6:
        return 'core'
    if has_cis and config_rules:
        return 'core'

    # Recommended
    if config_rules and major_count >= 3:
        return 'recommended'
    if has_security_hub and major_count >= 2:
        return 'recommended'
    if config_rules and has_security_hub:
        return 'recommended'
    if config_rules:
        return 'recommended'

    return 'enhanced'


def main():
    path = 'backend/compliance_discovery/csf_aws_mappings.json'
    with open(path) as f:
        data = json.load(f)

    # Step 1: Collect richest metadata for each control_id
    best_meta = {}  # control_id -> {frameworks, config_rules, security_hub, control_tower}
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

    # Step 2: Apply richest metadata everywhere
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

    print(f'Normalized framework metadata for {normalized} control instances')

    # Step 3: Re-classify and sort
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
    print(f'\nClassification results ({total} total):')
    print(f'  Core:        {stats["core"]}')
    print(f'  Recommended: {stats["recommended"]}')
    print(f'  Enhanced:    {stats["enhanced"]}')

    # Show subcategories with core controls
    with_core = []
    without_core = []
    for key, controls in sorted(data['controls'].items()):
        core_count = sum(1 for c in controls if c.get('priority') == 'core')
        if core_count > 0:
            with_core.append((key, core_count, len(controls)))
        elif len(controls) > 0:
            without_core.append(key)

    print(f'\nSubcategories with core controls: {len(with_core)}')
    for subcat, core, total in with_core[:15]:
        print(f'  {subcat}: {core} core / {total} total')
    if len(with_core) > 15:
        print(f'  ... and {len(with_core) - 15} more')

    print(f'\nSubcategories with controls but 0 core: {len(without_core)}')

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'\nSaved to {path}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Replace PR.DS-01 AWS control mappings with real AWS Control Guide entries.

PR.DS-01: "The confidentiality, integrity, and availability of data-at-rest
are protected."

Organized around three pillars:
1. Confidentiality (Encryption) - SSE, KMS, EBS, RDS, DynamoDB encryption
2. Integrity (Immutability) - S3 versioning, Object Lock (WORM)
3. Availability (Backups & Replication) - AWS Backup, RDS/EBS backups, S3 CRR
"""

import json

# All entries verified via ControlCompass MCP O(1) managed control lookup
PRDS01_REAL_CONTROLS = [
    # === 1. Confidentiality: Storage & Object Encryption ===
    {
        "control_id": "AWS-CG-0000057",
        "title": "Enable encryption on Amazon S3 buckets",
        "description": "Enable server-side encryption in S3 buckets to reduce the risk of unintentional data exposure. Enforces data-at-rest confidentiality.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"],
        "security_hub_controls": ["S3.4"],
        "control_tower_ids": ["CONFIG.S3.DT.8"],
        "frameworks": ["AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000059",
        "title": "Enable KMS encryption of new objects stored in Amazon S3 buckets",
        "description": "Encrypt new objects at rest in S3 buckets using an AWS KMS managed key to provide tighter access control over encryption keys.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_DEFAULT_ENCRYPTION_KMS"],
        "security_hub_controls": ["S3.17"],
        "control_tower_ids": ["SH.S3.17"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },
    # === 1b. Confidentiality: Block Storage Encryption ===
    {
        "control_id": "AWS-CG-0000034",
        "title": "Enable encryption at rest on Amazon EBS volumes attached to EC2 instances",
        "description": "Enable encryption at rest on EBS volumes attached to EC2 instances to protect data from unauthorized access.",
        "services": ["Amazon Elastic Block Store"],
        "config_rules": ["ENCRYPTED_VOLUMES"],
        "security_hub_controls": ["EC2.3"],
        "control_tower_ids": ["AWS-GR_ENCRYPTED_VOLUMES", "SH.EC2.3"],
        "frameworks": ["AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000033",
        "title": "Enable Amazon EBS default encryption",
        "description": "Enable Amazon EBS default encryption for volumes to protect confidentiality and integrity of data at rest account-wide.",
        "services": ["Amazon Elastic Block Store"],
        "config_rules": ["EC2_EBS_ENCRYPTION_BY_DEFAULT"],
        "security_hub_controls": ["EC2.7"],
        "control_tower_ids": ["SH.EC2.7"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },
    # === 1c. Confidentiality: Database Encryption ===
    {
        "control_id": "AWS-CG-0000193",
        "title": "Enable encryption at rest for Amazon RDS database instances",
        "description": "Enable encryption at rest for Amazon RDS DB instances to secure data from unauthorized access to the underlying storage.",
        "services": ["Amazon RDS"],
        "config_rules": ["RDS_STORAGE_ENCRYPTED"],
        "security_hub_controls": ["RDS.3"],
        "control_tower_ids": ["AWS-GR_RDS_STORAGE_ENCRYPTED", "SH.RDS.3"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },
    {
        "control_id": "AWS-CG-0000328",
        "title": "Enable encryption at rest for Amazon RDS clusters",
        "description": "Enable encryption at rest for Amazon RDS clusters to reduce the risk of unauthorized access to data stored in Aurora and other cluster-based databases.",
        "services": ["Amazon RDS"],
        "config_rules": ["RDS_CLUSTER_ENCRYPTED_AT_REST"],
        "security_hub_controls": ["RDS.27"],
        "control_tower_ids": ["SH.RDS.27"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000103",
        "title": "Encrypt data at rest using AWS KMS in Amazon DynamoDB",
        "description": "Encrypt customer data at rest in Amazon DynamoDB using AWS KMS to maintain confidentiality and prevent unauthorized data exposure.",
        "services": ["Amazon DynamoDB"],
        "config_rules": ["DYNAMODB_TABLE_ENCRYPTED_KMS"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.DYNAMODB.DT.4"],
        "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    # === 2. Integrity: Immutability & Versioning ===
    {
        "control_id": "AWS-CG-0000168",
        "title": "Enable versioning and MFA delete on Amazon S3 buckets",
        "description": "Enable versioning on S3 buckets to protect objects from unintentional deletion and data loss. Enable MFA delete to require additional steps in the deletion process.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_BUCKET_VERSIONING_ENABLED"],
        "security_hub_controls": ["S3.14"],
        "control_tower_ids": ["AWS-GR_S3_VERSIONING_ENABLED"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CIS-AWS-Benchmark-v1.4", "FedRAMP-r4", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1"]
    },
    {
        "control_id": "AWS-CG-0000207",
        "title": "Enable Amazon S3 bucket object lock",
        "description": "Enable object lock in S3 buckets to enforce WORM (Write Once Read Many) protection against unintentional object changes or deletions.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_BUCKET_DEFAULT_LOCK_ENABLED"],
        "security_hub_controls": ["S3.15"],
        "control_tower_ids": ["CONFIG.S3.DT.9"],
        "frameworks": ["AWS-WAF-v10", "FedRAMP-r4", "NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
    },
    # === 3. Availability: Backups & Replication ===
    {
        "control_id": "AWS-CG-0000076",
        "title": "Configure backup plans for AWS Backup with required frequency and retention",
        "description": "Configure backup plans for AWS Backup according to the required frequency and retention period to prevent data loss.",
        "services": ["AWS Backup"],
        "config_rules": ["BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK"],
        "security_hub_controls": [],
        "control_tower_ids": ["BACKUP_PLAN_MIN_FREQUENCY_AND_MIN_RETENTION_CHECK"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "CIS-v7.1", "CIS-v8.0", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000195",
        "title": "Backup Amazon RDS instances",
        "description": "Configure automatic backups of Amazon RDS instances to prevent data loss and support recovery efforts in the event of a disruption.",
        "services": ["Amazon RDS"],
        "config_rules": ["DB_INSTANCE_BACKUP_ENABLED", "RDS_IN_BACKUP_PLAN", "RDS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
        "security_hub_controls": ["RDS.11", "RDS.26"],
        "control_tower_ids": ["CONFIG.RDS.DT.15", "CONFIG.RDS.DT.20", "SH.RDS.11"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CCCS-Medium-Cloud-Control-May-2019", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5"]
    },
    {
        "control_id": "AWS-CG-0000152",
        "title": "Backup Amazon EBS volumes",
        "description": "Configure automatic backups for Amazon EBS volumes to prevent data loss and support recovery efforts in the event of a disruption.",
        "services": ["Amazon Elastic Block Store"],
        "config_rules": ["EBS_IN_BACKUP_PLAN", "EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
        "security_hub_controls": ["EC2.28"],
        "control_tower_ids": ["CONFIG.EC2.DT.14", "CONFIG.EC2.DT.6"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5"]
    },
    {
        "control_id": "AWS-CG-0000205",
        "title": "Enable Amazon S3 Cross-Region Replication (CRR)",
        "description": "Enable S3 CRR to provide data redundancy for disaster recovery, ensuring data availability across AWS Regions.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_BUCKET_REPLICATION_ENABLED"],
        "security_hub_controls": ["S3.7"],
        "control_tower_ids": ["CONFIG.S3.DT.1"],
        "frameworks": ["ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5"]
    },
]


def main():
    mappings_path = 'backend/compliance_discovery/csf_aws_mappings.json'
    with open(mappings_path) as f:
        data = json.load(f)

    old_controls = data['controls'].get('pr.ds-01', [])
    old_ids = [c['control_id'] for c in old_controls]
    print(f"Current PR.DS-01: {len(old_controls)} controls")
    print(f"  IDs: {old_ids}")

    old_with_rules = sum(1 for c in old_controls if c.get('config_rules'))
    print(f"  With config rules: {old_with_rules}/{len(old_controls)}")

    # Replace with real controls
    data['controls']['pr.ds-01'] = PRDS01_REAL_CONTROLS

    new_ids = [c['control_id'] for c in PRDS01_REAL_CONTROLS]
    new_with_rules = sum(1 for c in PRDS01_REAL_CONTROLS if c.get('config_rules'))
    print(f"\nNew PR.DS-01: {len(PRDS01_REAL_CONTROLS)} controls")
    print(f"  IDs: {new_ids}")
    print(f"  With config rules: {new_with_rules}/{len(PRDS01_REAL_CONTROLS)}")

    total_rules = sum(len(c.get('config_rules', [])) for c in PRDS01_REAL_CONTROLS)
    total_hub = sum(len(c.get('security_hub_controls', [])) for c in PRDS01_REAL_CONTROLS)
    total_ct = sum(len(c.get('control_tower_ids', [])) for c in PRDS01_REAL_CONTROLS)
    print(f"  Total Config rules: {total_rules}")
    print(f"  Total Security Hub controls: {total_hub}")
    print(f"  Total Control Tower IDs: {total_ct}")

    # Update metadata
    data['metadata']['total_controls'] = sum(len(v) for v in data['controls'].values())

    with open(mappings_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nUpdated {mappings_path}")


if __name__ == '__main__':
    main()

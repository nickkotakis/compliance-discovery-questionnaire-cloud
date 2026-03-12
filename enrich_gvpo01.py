#!/usr/bin/env python3
"""Replace synthetic GV.PO-01 AWS control mappings with real AWS Control Guide entries.

GV.PO-01 requires that cybersecurity policies are "established, communicated, and enforced."
Since policy covers the entire security spectrum, we map real AWS Config rules that prove
enforcement of common enterprise security policies:

1. Data Protection & Encryption Policy
2. Identity and Access Management (IAM) Policy
3. Auditing and Logging Policy
4. Network Security & Public Exposure Policy
5. Security Monitoring Policy
"""

import json

# Real AWS Control Guide entries sourced from ControlCompass MCP server
# Each entry verified via O(1) managed control lookup
GVPO01_REAL_CONTROLS = [
    # === 1. Data Protection & Encryption Policy ===
    {
        "control_id": "AWS-CG-0000057",
        "title": "Enable encryption on Amazon S3 buckets",
        "description": "Enable server-side encryption in S3 buckets to reduce the risk of unintentional data exposure. Enforces data-at-rest encryption policy.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"],
        "security_hub_controls": ["S3.4"],
        "control_tower_ids": ["CONFIG.S3.DT.8"],
        "frameworks": ["AWS-WAF-v10", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000193",
        "title": "Enable encryption at rest for Amazon RDS database instances",
        "description": "Enable encryption at rest for Amazon RDS DB instances to secure data from unauthorized access to the underlying storage. Enforces data-at-rest encryption policy.",
        "services": ["Amazon RDS"],
        "config_rules": ["RDS_STORAGE_ENCRYPTED"],
        "security_hub_controls": ["RDS.3"],
        "control_tower_ids": ["AWS-GR_RDS_STORAGE_ENCRYPTED", "SH.RDS.3"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },
    {
        "control_id": "AWS-CG-0000034",
        "title": "Enable encryption at rest on Amazon EBS volumes attached to EC2 instances",
        "description": "Enable encryption at rest on EBS volumes attached to EC2 instances to protect data from unauthorized access. Enforces data-at-rest encryption policy.",
        "services": ["Amazon Elastic Block Store"],
        "config_rules": ["ENCRYPTED_VOLUMES"],
        "security_hub_controls": ["EC2.3"],
        "control_tower_ids": ["AWS-GR_ENCRYPTED_VOLUMES", "SH.EC2.3"],
        "frameworks": ["AWS-WAF-v10", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000055",
        "title": "Encrypt Amazon CloudWatch log groups",
        "description": "Encrypt all log data stored in CloudWatch Logs to protect the confidentiality and integrity of audit logs. Enforces data-at-rest encryption policy.",
        "services": ["Amazon CloudWatch Logs"],
        "config_rules": ["CLOUDWATCH_LOG_GROUP_ENCRYPTED"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.LOGS.DT.1"],
        "frameworks": ["FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },

    # === 2. Identity and Access Management (IAM) Policy ===
    {
        "control_id": "AWS-CG-0000187",
        "title": "Configure Multi-Factor Authentication (MFA) for IAM users",
        "description": "Configure MFA for IAM users to protect resources from unauthorized access. Enforces IAM authentication policy.",
        "services": ["AWS Identity and Access Management"],
        "config_rules": ["IAM_USER_MFA_ENABLED"],
        "security_hub_controls": ["IAM.19"],
        "control_tower_ids": ["AWS-GR_IAM_USER_MFA_ENABLED"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000138",
        "title": "Enable MFA for IAM users that have a console password",
        "description": "Enable MFA for IAM users with console passwords to strengthen user authentication. Enforces IAM authentication policy.",
        "services": ["AWS Identity and Access Management"],
        "config_rules": ["MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"],
        "security_hub_controls": ["IAM.5"],
        "control_tower_ids": ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS", "SH.IAM.5"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "AWS-WAF-v10", "CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000048",
        "title": "Implement multi-factor authentication (MFA) for the AWS root account",
        "description": "Enable MFA for the AWS root account to reduce the potential for brute-force attacks and unauthorized access. Enforces IAM authentication policy.",
        "services": ["AWS Identity and Access Management"],
        "config_rules": ["ROOT_ACCOUNT_MFA_ENABLED"],
        "security_hub_controls": ["IAM.9"],
        "control_tower_ids": ["AWS-GR_ROOT_ACCOUNT_MFA_ENABLED"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000182",
        "title": "Disable the access keys for the AWS root user",
        "description": "Disable AWS root user access keys to prevent unauthorized access to the AWS environment. Enforces IAM access control policy.",
        "services": ["AWS Identity and Access Management"],
        "config_rules": ["IAM_ROOT_ACCESS_KEY_CHECK"],
        "security_hub_controls": ["IAM.4"],
        "control_tower_ids": ["AWS-GR_RESTRICT_ROOT_USER_ACCESS_KEYS", "SH.IAM.4"],
        "frameworks": ["AWS-WAF-v10", "CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v8.0", "ISO-IEC-27001:2013-Annex-A"]
    },
    {
        "control_id": "AWS-CG-0000184",
        "title": "Enforce account password policy for IAM users",
        "description": "Define strong password parameters within the AWS account password policy to enforce minimum password requirements. Enforces IAM authentication policy.",
        "services": ["AWS Identity and Access Management"],
        "config_rules": ["IAM_PASSWORD_POLICY"],
        "security_hub_controls": ["IAM.10"],
        "control_tower_ids": ["SH.IAM.7"],
        "frameworks": ["CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },

    # === 3. Auditing and Logging Policy ===
    {
        "control_id": "AWS-CG-0000012",
        "title": "Enable AWS CloudTrail for all regions",
        "description": "Enable CloudTrail to capture all API call activity logs across all Regions, providing visibility for monitoring all AWS resources and services. Enforces auditing and logging policy.",
        "services": ["AWS CloudTrail"],
        "config_rules": ["MULTI_REGION_CLOUD_TRAIL_ENABLED"],
        "security_hub_controls": ["CloudTrail.1"],
        "control_tower_ids": ["SH.CloudTrail.1"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "CIS-v7.1", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000009",
        "title": "Enable security trails in AWS CloudTrail",
        "description": "Enable and create security trails in AWS CloudTrail to retain and protect audit logs of AWS API call activity. Enforces auditing and logging policy.",
        "services": ["AWS CloudTrail"],
        "config_rules": ["CLOUDTRAIL_SECURITY_TRAIL_ENABLED"],
        "security_hub_controls": ["CloudTrail.3"],
        "control_tower_ids": ["CONFIG.CLOUDTRAIL.DT.6"],
        "frameworks": ["ACSC-Essential-Eight-Nov-2022", "ACSC-ISM-02-Mar-2023", "FedRAMP-r4", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000062",
        "title": "Enable Amazon VPC flow logs in all VPCs",
        "description": "Enable all Amazon VPC flow logs and recording to aid in anomalous traffic detection. Enforces auditing and logging policy.",
        "services": ["Amazon Virtual Private Cloud"],
        "config_rules": ["VPC_FLOW_LOGS_ENABLED"],
        "security_hub_controls": ["EC2.6"],
        "control_tower_ids": ["SH.EC2.6"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "CIS-v7.1", "CIS-v8.0", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },

    # === 4. Network Security & Public Exposure Policy ===
    {
        "control_id": "AWS-CG-0000198",
        "title": "Block public access to Amazon S3 buckets",
        "description": "Configure Amazon S3 to block public access to S3 buckets to protect data from unauthorized access. Enforces network security and public exposure policy.",
        "services": ["Amazon S3"],
        "config_rules": ["S3_BUCKET_PUBLIC_READ_PROHIBITED", "S3_BUCKET_PUBLIC_WRITE_PROHIBITED", "S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS", "S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED"],
        "security_hub_controls": ["S3.1", "S3.2", "S3.3", "S3.8"],
        "control_tower_ids": ["AWS-GR_S3_BUCKET_PUBLIC_READ_PROHIBITED", "AWS-GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED", "CT.S3.PR.1", "SH.S3.1", "SH.S3.2", "SH.S3.3", "SH.S3.8"],
        "frameworks": ["AWS-WAF-v10", "CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "ISO-IEC-27001:2013-Annex-A", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },
    {
        "control_id": "AWS-CG-0000063",
        "title": "Do not use default security group rules in Amazon VPC",
        "description": "Change VPC default security group rules from their default configuration to prevent unrestricted inbound/outbound traffic. Enforces network security policy.",
        "services": ["Amazon Virtual Private Cloud"],
        "config_rules": ["VPC_DEFAULT_SECURITY_GROUP_CLOSED"],
        "security_hub_controls": ["EC2.2"],
        "control_tower_ids": ["SH.EC2.2"],
        "frameworks": ["CIS-AWS-Benchmark-v1.2", "CIS-AWS-Benchmark-v1.3", "CIS-AWS-Benchmark-v1.4", "FedRAMP-r4", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },
    {
        "control_id": "AWS-CG-0000093",
        "title": "Restrict inbound traffic on sensitive ports in EC2 security groups",
        "description": "Change the AWS default security groups for Amazon EC2 instances and allow only authorized connections, blocking all other traffic. Enforces network security policy.",
        "services": ["Amazon EC2"],
        "config_rules": ["RESTRICTED_INCOMING_TRAFFIC"],
        "security_hub_controls": ["EC2.14"],
        "control_tower_ids": ["AWS-GR_RESTRICTED_COMMON_PORTS"],
        "frameworks": ["CIS-v7.1", "FedRAMP-r4", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0"]
    },

    # === 5. Security Monitoring Policy ===
    {
        "control_id": "AWS-CG-0000180",
        "title": "Enable Amazon GuardDuty in AWS account and region",
        "description": "Implement intrusion detection capabilities by enabling GuardDuty to monitor for and detect suspicious activity. Enforces security monitoring policy.",
        "services": ["Amazon GuardDuty"],
        "config_rules": ["GUARDDUTY_ENABLED_CENTRALIZED"],
        "security_hub_controls": ["GuardDuty.1"],
        "control_tower_ids": ["SH.GuardDuty.1"],
        "frameworks": ["ACSC-ISM-02-Mar-2023", "AWS-WAF-v10", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-171-r2", "NIST-SP-800-53-r5", "PCI-DSS-v3.2.1", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
    {
        "control_id": "AWS-CG-0000169",
        "title": "Enable AWS Security Hub service",
        "description": "Activate Security Hub to receive findings from supported AWS security services for centralized security posture management. Enforces security monitoring policy.",
        "services": ["AWS Security Hub"],
        "config_rules": ["SECURITYHUB_ENABLED"],
        "security_hub_controls": [],
        "control_tower_ids": ["CONFIG.SECURITYHUB.DT.1"],
        "frameworks": ["AWS-WAF-v10", "CIS-v7.1", "CIS-v8.0", "FedRAMP-r4", "NIST-CSF-v1.1", "NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
    },
]


def main():
    # Load current CSF AWS mappings
    mappings_path = 'backend/compliance_discovery/csf_aws_mappings.json'
    with open(mappings_path) as f:
        data = json.load(f)

    old_controls = data['controls'].get('gv.po-01', [])
    old_ids = [c['control_id'] for c in old_controls]
    print(f"Current GV.PO-01: {len(old_controls)} controls")
    print(f"  IDs: {old_ids}")

    # Count how many had real config rules
    old_with_rules = sum(1 for c in old_controls if c.get('config_rules'))
    print(f"  With config rules: {old_with_rules}/{len(old_controls)}")

    # Replace with real controls
    data['controls']['gv.po-01'] = GVPO01_REAL_CONTROLS

    new_ids = [c['control_id'] for c in GVPO01_REAL_CONTROLS]
    new_with_rules = sum(1 for c in GVPO01_REAL_CONTROLS if c.get('config_rules'))
    print(f"\nNew GV.PO-01: {len(GVPO01_REAL_CONTROLS)} controls")
    print(f"  IDs: {new_ids}")
    print(f"  With config rules: {new_with_rules}/{len(GVPO01_REAL_CONTROLS)}")

    # Count total config rules
    total_rules = sum(len(c.get('config_rules', [])) for c in GVPO01_REAL_CONTROLS)
    total_hub = sum(len(c.get('security_hub_controls', [])) for c in GVPO01_REAL_CONTROLS)
    total_ct = sum(len(c.get('control_tower_ids', [])) for c in GVPO01_REAL_CONTROLS)
    print(f"  Total Config rules: {total_rules}")
    print(f"  Total Security Hub controls: {total_hub}")
    print(f"  Total Control Tower IDs: {total_ct}")

    # Update metadata
    data['metadata']['total_controls'] = sum(len(v) for v in data['controls'].values())

    # Write back
    with open(mappings_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nUpdated {mappings_path}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Script to populate aws_controls_mcp_data.json with AWS control mappings for NIST controls.

This script processes MCP search results and organizes them by NIST control ID.
"""

import json
from datetime import datetime
from pathlib import Path

# MCP search results for key NIST controls
MCP_RESULTS = {
    "ac-2": {  # Account Management - IAM
        "search_query": "IAM user management account",
        "controls": [
            {
                "control_id": "AWS-CG-0000138",
                "title": "Enable MFA for AWS Identity and Access Management (IAM) users that have a console password",
                "description": "Enable MFA for IAM users that have a console password in order to strengthen user authentication.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": ["MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"],
                "security_hub_controls": ["IAM.5"],
                "control_tower_ids": ["AWS-GR_MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS", "SH.IAM.5"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000183",
                "title": "Ensure all AWS Identity and Access Management (IAM) user groups contain users",
                "description": "Ensure that all IAM user groups contain users, or remove empty user groups when no longer needed so the groups cannot be used to unintentionally grant access.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": ["IAM_GROUP_HAS_USERS_CHECK"],
                "security_hub_controls": [],
                "control_tower_ids": ["CONFIG.IAM.DT.6"],
                "frameworks": ["NIST-SP-800-53-r5"]
            },
            {
                "control_id": "AWS-CG-0000185",
                "title": "Manage access in AWS by creating policies and attaching them to AWS Identity and Access Management (IAM) identities",
                "description": "Manage access in AWS by creating and attaching IAM policies to ensure that only authorized individuals have access to data and resources.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": ["IAM_POLICY_IN_USE"],
                "security_hub_controls": ["IAM.18"],
                "control_tower_ids": [],
                "frameworks": ["NIST-SP-800-53-r5", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000187",
                "title": "Configure Multi-Factor Authentication (MFA) for AWS Identity and Access Management (IAM) users",
                "description": "Configure MFA for IAM users to protect resources from unauthorized access.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": ["IAM_USER_MFA_ENABLED"],
                "security_hub_controls": ["IAM.19"],
                "control_tower_ids": ["AWS-GR_IAM_USER_MFA_ENABLED"],
                "frameworks": ["SSAE-18-SOC-2-Oct-2023", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000479",
                "title": "Prevent IAM inline policies from using wildcard permissions in both Action and Resource elements",
                "description": "Restrict IAM inline policies from including 'Effect' 'Allow' with 'Action' '*' over 'Resource' '*' to enforce least privilege access.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["CT.IAM.PR.1"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000574",
                "title": "Enforce IAM password policy to require at least one uppercase letter",
                "description": "Enforces that IAM password policies require at least one uppercase letter in passwords, strengthening authentication security against brute force attacks.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": [],
                "security_hub_controls": ["IAM.11"],
                "control_tower_ids": [],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000575",
                "title": "Enforce strong password policies for AWS Identity and Access Management (IAM)",
                "description": "Requires IAM user password policies to implement strong configurations, preventing the use of weak passwords and reducing the risk of unauthorized access.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": [],
                "security_hub_controls": ["IAM.7"],
                "control_tower_ids": [],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000581",
                "title": "Enforce IAM password policy to require at least one lowercase letter",
                "description": "Enforces that IAM password policies require at least one lowercase letter in passwords to strengthen authentication security.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": [],
                "security_hub_controls": ["IAM.12"],
                "control_tower_ids": [],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000760",
                "title": "Ensure IAM users do not have policies directly attached in AWS Identity and Access Management (IAM)",
                "description": "Enforce IAM users to inherit permissions from IAM groups or roles rather than having inline or managed policies directly attached.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["CT.IAM.PR.4"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000761",
                "title": "Restrict IAM inline policies from using wildcard service actions in AWS Identity and Access Management (IAM)",
                "description": "Restrict IAM inline policies from using 'Effect' 'Allow' with wildcard service actions to enforce least privilege access.",
                "services": ["AWS Identity and Access Management"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["CT.IAM.PR.5"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            }
        ]
    },
    "au-2": {  # Audit Events - CloudTrail
        "search_query": "CloudTrail logging audit events",
        "controls": [
            {
                "control_id": "AWS-CG-0000008",
                "title": "Configure AWS CloudTrail trails to be multi-region",
                "description": "Configure CloudTrail to support multi-Region trails in order to centralize log aggregation of all events for audit log reviews.",
                "services": ["AWS CloudTrail"],
                "config_rules": ["MULTI_REGION_CLOUD_TRAIL_ENABLED"],
                "security_hub_controls": ["CloudTrail.1"],
                "control_tower_ids": ["SH.CloudTrail.1"],
                "frameworks": ["NIST-SP-800-53-r5", "ISO-IEC-27001:2013-Annex-A", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000009",
                "title": "Enable security trails in AWS CloudTrail",
                "description": "Enable and create security trails in AWS CloudTrail to retain and protect audit logs of AWS API call activity.",
                "services": ["AWS CloudTrail"],
                "config_rules": ["CLOUDTRAIL_SECURITY_TRAIL_ENABLED"],
                "security_hub_controls": ["CloudTrail.3"],
                "control_tower_ids": ["CONFIG.CLOUDTRAIL.DT.6"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000014",
                "title": "Enable log file validation for AWS CloudTrail logs",
                "description": "Protect log files generated by CloudTrail against tampering or unauthorized modifications in order to support log file integrity and reliability.",
                "services": ["AWS CloudTrail"],
                "config_rules": ["CLOUD_TRAIL_LOG_FILE_VALIDATION_ENABLED"],
                "security_hub_controls": ["CloudTrail.4"],
                "control_tower_ids": ["CT.CLOUDTRAIL.PR.2", "SH.CloudTrail.4"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000010",
                "title": "Configure AWS CloudTrail to send logs to Amazon CloudWatch Logs",
                "description": "Configure CloudTrail to send logs to CloudWatch Logs in order to monitor activity trails and notify when potentially anomalous activity occurs.",
                "services": ["AWS CloudTrail"],
                "config_rules": ["CLOUD_TRAIL_CLOUD_WATCH_LOGS_ENABLED"],
                "security_hub_controls": ["CloudTrail.5"],
                "control_tower_ids": ["AWS-GR_CLOUDTRAIL_CLOUDWATCH_LOGS_ENABLED", "SH.CloudTrail.5"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v3.2.1"]
            },
            {
                "control_id": "AWS-CG-0000013",
                "title": "Enable encryption for AWS CloudTrail trails",
                "description": "Encrypt all log data generated by CloudTrail while at rest to protect the confidentiality and integrity of the log data stored in CloudTrail.",
                "services": ["AWS CloudTrail"],
                "config_rules": ["CLOUD_TRAIL_ENCRYPTION_ENABLED"],
                "security_hub_controls": ["CloudTrail.2"],
                "control_tower_ids": ["SH.CloudTrail.2"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            }
        ]
    },
    "sc-7": {  # Boundary Protection - Security Groups
        "search_query": "security groups boundary protection network",
        "controls": [
            {
                "control_id": "AWS-CG-0000155",
                "title": "Remove unused Amazon EC2 security groups",
                "description": "Review and remove unused EC2 security groups to reduce complexity in network management and improve network security and performance.",
                "services": ["Amazon EC2"],
                "config_rules": ["EC2_SECURITY_GROUP_ATTACHED_TO_ENI", "EC2_SECURITY_GROUP_ATTACHED_TO_ENI_PERIODIC"],
                "security_hub_controls": ["EC2.22"],
                "control_tower_ids": ["CONFIG.EC2.DT.11", "SH.EC2.22"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000063",
                "title": "Do not use default security group rules in Amazon Virtual Private Cloud (VPC)",
                "description": "Change VPC default security groups rules from their default configuration and ensure defaults are not used to prevent unrestricted inbound/outbound traffic.",
                "services": ["Amazon VPC Lattice"],
                "config_rules": ["VPC_DEFAULT_SECURITY_GROUP_CLOSED"],
                "security_hub_controls": ["EC2.2"],
                "control_tower_ids": ["SH.EC2.2"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
            },
            {
                "control_id": "AWS-CG-0000325",
                "title": "Deploy firewalls managed through AWS Network firewalls across multiple Availability Zones",
                "description": "Deploy firewalls managed through AWS Network firewalls across multiple Availability Zones to provide redundancy, scalability and improved availability.",
                "services": ["AWS Network Firewall"],
                "config_rules": ["NETFW_MULTI_AZ_ENABLED"],
                "security_hub_controls": ["NetworkFirewall.1"],
                "control_tower_ids": ["CONFIG.NETWORK-FIREWALL.DT.3"],
                "frameworks": ["NIST-SP-800-53-r5", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000247",
                "title": "Define a default action for handling stateless, fragmented packets in AWS Network Firewall policies",
                "description": "Define a default action for handling stateless, fragmented packets in Network Firewall policies that match defined control parameters.",
                "services": ["AWS Network Firewall"],
                "config_rules": ["NETFW_POLICY_DEFAULT_ACTION_FRAGMENT_PACKETS", "NETFW_POLICY_DEFAULT_ACTION_FULL_PACKETS"],
                "security_hub_controls": ["NetworkFirewall.4"],
                "control_tower_ids": ["SH.NetworkFirewall.4"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000229",
                "title": "Configure custom TLS policies for listeners on AWS Elastic Load Balancers",
                "description": "Configure custom TLS policies for listeners on AWS Elastic Load Balancer to customize security settings according to specific requirements and specific cipher standards.",
                "services": ["AWS Elastic Load Balancing"],
                "config_rules": ["ELB_CUSTOM_SECURITY_POLICY_SSL_CHECK", "ELB_PREDEFINED_SECURITY_POLICY_SSL_CHECK", "ELB_TLS_HTTPS_LISTENERS_ONLY"],
                "security_hub_controls": ["ELB.3", "ELB.8"],
                "control_tower_ids": ["SH.ELB.3", "SH.ELB.8"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            }
        ]
    },
    "cp-9": {  # Backup - AWS Backup, EBS, RDS, S3
        "search_query": "backup EBS RDS S3 recovery",
        "controls": [
            {
                "control_id": "AWS-CG-0000152",
                "title": "Backup Amazon Elastic Block Storage (EBS) volumes",
                "description": "Configure automatic backups for Amazon EBS volumes in order to prevent data loss and support recovery efforts in the event of a disruption.",
                "services": ["Amazon Elastic Block Store"],
                "config_rules": ["EBS_IN_BACKUP_PLAN", "EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
                "security_hub_controls": ["EC2.28"],
                "control_tower_ids": ["CONFIG.EC2.DT.14", "CONFIG.EC2.DT.6"],
                "frameworks": ["NIST-SP-800-53-r5"]
            },
            {
                "control_id": "AWS-CG-0000379",
                "title": "Ensure Amazon RDS database instances have automatic backups configured with retention period of at least 7 days",
                "description": "Require Amazon RDS database instances to have automated backups enabled with a backup retention period greater than or equal to seven days.",
                "services": ["Amazon RDS"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["CT.RDS.PR.8"],
                "frameworks": ["NIST-SP-800-53-r5", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000267",
                "title": "Configure AWS Backup Plan for Amazon S3 resources",
                "description": "Configure AWS Backup Plan for Amazon S3 resources to mitigate data loss and provide data protection.",
                "services": ["Amazon S3"],
                "config_rules": ["S3_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
                "security_hub_controls": [],
                "control_tower_ids": ["CONFIG.S3.DT.3"],
                "frameworks": ["NIST-SP-800-53-r5"]
            },
            {
                "control_id": "AWS-CG-0000275",
                "title": "Enable encryption at rest for AWS Backup recovery points",
                "description": "Enable encryption at rest for AWS Backup recovery points to reduce the risk of unauthorized access to data.",
                "services": ["AWS Backup"],
                "config_rules": ["BACKUP_RECOVERY_POINT_ENCRYPTED"],
                "security_hub_controls": ["Backup.1"],
                "control_tower_ids": [],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000109",
                "title": "Configure recovery points for AWS Backup such that they do not expire before the retention period",
                "description": "Configure recovery points for AWS Backup such that they do not expire before the retention period in order to prevent data loss and meet retention requirements.",
                "services": ["AWS Backup"],
                "config_rules": ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"],
                "security_hub_controls": [],
                "control_tower_ids": ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"],
                "frameworks": []
            }
        ]
    },
    "sc-28": {  # Data at Rest Protection - Encryption
        "search_query": "encryption KMS data protection",
        "controls": [
            {
                "control_id": "AWS-CG-0000103",
                "title": "Encrypt data at rest using AWS Key Management Service (KMS) in Amazon DynamoDB",
                "description": "Encrypt customer data at rest in Amazon DynamoDB using AWS KMS to maintain confidentiality and prevent unauthorized data exposure.",
                "services": ["Amazon DynamoDB"],
                "config_rules": ["DYNAMODB_TABLE_ENCRYPTED_KMS"],
                "security_hub_controls": [],
                "control_tower_ids": ["CONFIG.DYNAMODB.DT.4"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000587",
                "title": "Ensure Amazon RDS database clusters have encryption at rest configured",
                "description": "Enforce that Amazon Relational Database Service (RDS) database clusters are configured with storage encryption at rest.",
                "services": ["Amazon RDS"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["CT.RDS.PR.16"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000762",
                "title": "Ensure Amazon Kinesis data streams have encryption at rest configured",
                "description": "Enforce server-side encryption for Amazon Kinesis data streams to automatically encrypt data before it is written to storage.",
                "services": ["Amazon Kinesis Data Streams"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["CT.KINESIS.PR.1"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000565",
                "title": "Prevent public access in AWS KMS key policies",
                "description": "Configure AWS KMS key policies to prohibit public access to encryption keys. This ensures that KMS keys remain private and accessible only to authorized entities.",
                "services": ["AWS Key Management Service"],
                "config_rules": ["KMS_KEY_POLICY_NO_PUBLIC_ACCESS"],
                "security_hub_controls": [],
                "control_tower_ids": ["CONFIG.KMS.DT.2"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000233",
                "title": "Encrypt Amazon OpenSearch Service node communications",
                "description": "Encrypt OpenSearch end-to-end node communication by using a secure protocol to protect data from unauthorized disclosure.",
                "services": ["Amazon OpenSearch Service"],
                "config_rules": ["ELASTICSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK", "OPENSEARCH_HTTPS_REQUIRED", "OPENSEARCH_NODE_TO_NODE_ENCRYPTION_CHECK"],
                "security_hub_controls": ["ES.3", "ES.8", "Opensearch.3", "Opensearch.8"],
                "control_tower_ids": ["SH.ES.3", "SH.ES.8", "SH.Opensearch.3", "SH.Opensearch.8"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            }
        ]
    },
    "cm-2": {  # Baseline Configuration - AWS Config
        "search_query": "Config baseline configuration management",
        "controls": [
            {
                "control_id": "AWS-CG-0000466",
                "title": "Prevent unauthorized changes to AWS Config settings",
                "description": "Blocks all users and roles, except the AWS Control Tower service role, from modifying or disabling AWS Config settings across the organization.",
                "services": ["AWS Config"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["AWS-GR_CONFIG_CHANGE_PROHIBITED"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000465",
                "title": "Prevent unauthorized modifications to AWS Config Rules managed by Control Tower",
                "description": "Blocks all users and roles, except the AWS Control Tower service role, from modifying or deleting AWS Config rules and configuration aggregators.",
                "services": ["AWS Config"],
                "config_rules": [],
                "security_hub_controls": [],
                "control_tower_ids": ["AWS-GR_CONFIG_RULE_CHANGE_PROHIBITED"],
                "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
            },
            {
                "control_id": "AWS-CG-0000152",
                "title": "Backup Amazon Elastic Block Storage (EBS) volumes",
                "description": "Configure automatic backups for Amazon EBS volumes in order to prevent data loss and support recovery efforts in the event of a disruption.",
                "services": ["Amazon Elastic Block Store"],
                "config_rules": ["EBS_IN_BACKUP_PLAN", "EBS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
                "security_hub_controls": ["EC2.28"],
                "control_tower_ids": ["CONFIG.EC2.DT.14", "CONFIG.EC2.DT.6"],
                "frameworks": ["NIST-SP-800-53-r5"]
            }
        ]
    }
}


def main():
    """Generate the aws_controls_mcp_data.json file with all control mappings."""
    
    # Build the complete data structure
    data = {
        "metadata": {
            "export_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_controls_mapped": len(MCP_RESULTS),
            "mcp_server": "compass-control-guides-remote",
            "note": "AWS control mappings from MCP server for NIST 800-53 controls"
        },
        "controls": {}
    }
    
    # Add all controls organized by NIST control ID
    for nist_control_id, control_data in MCP_RESULTS.items():
        data["controls"][nist_control_id] = control_data["controls"]
    
    # Write to file
    output_path = Path(__file__).parent / "compliance_discovery" / "aws_controls_mcp_data.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Successfully generated {output_path}")
    print(f"📊 Total NIST controls mapped: {len(MCP_RESULTS)}")
    
    # Print summary
    total_aws_controls = sum(len(control_data["controls"]) for control_data in MCP_RESULTS.values())
    print(f"📋 Total AWS controls: {total_aws_controls}")
    print("\n🎯 Controls by NIST family:")
    for nist_id, control_data in MCP_RESULTS.items():
        print(f"  - {nist_id.upper()}: {len(control_data['controls'])} AWS controls")


if __name__ == "__main__":
    main()

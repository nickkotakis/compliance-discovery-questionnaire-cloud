#!/usr/bin/env python3
"""
Add final batch of AWS implementation guide data for remaining 6 high-priority controls.
Completes the AWS implementation guide population.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

def main():
    """Add AWS controls for AU-9, CM-7, AC-17, IR-8, CP-2, and CP-4."""
    
    # Load existing data
    data_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    print(f"Loaded existing data with {data['metadata']['total_controls_mapped']} controls")
    
    # AU-9: Protection of Audit Information (CloudTrail, S3)
    data['controls']['au-9'] = [
        {
            "control_id": "AWS-CG-0000774",
            "title": "Enforce retention policy for log archive in Amazon S3 buckets",
            "description": "Prevents unauthorized modification of lifecycle configurations for Amazon S3 buckets, ensuring data retention policies remain intact.",
            "services": ["Amazon S3"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": ["AWS-GR_AUDIT_BUCKET_RETENTION_POLICY"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
        },
        {
            "control_id": "AWS-CG-0000772",
            "title": "Prevent policy changes to log archive S3 buckets",
            "description": "Blocks unauthorized modification of bucket policies for long-term archive Amazon S3 buckets to preserve the integrity of audit logs.",
            "services": ["Amazon S3"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": ["AWS-GR_AUDIT_BUCKET_POLICY_CHANGES_PROHIBITED"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
        },
        {
            "control_id": "AWS-CG-0000078",
            "title": "Configure AWS CloudTrail logs in Amazon S3 buckets with no public access",
            "description": "Configure the CloudTrail logs S3 bucket with no public access to maintain log integrity and confidentiality.",
            "services": ["AWS CloudTrail"],
            "config_rules": ["S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED"],
            "security_hub_controls": ["CloudTrail.6", "S3.8"],
            "control_tower_ids": ["SH.CloudTrail.6", "SH.S3.8"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
        }
    ]
    
    # CM-7: Least Functionality (Security Groups, Network Controls)
    data['controls']['cm-7'] = [
        {
            "control_id": "AWS-CG-0000253",
            "title": "Disable automatic assignment of public IP addresses for Amazon VPC subnets",
            "description": "Disable automatic assignment of public IP addresses for Amazon VPC subnets to prevent instances from being accessed directly from the public Internet.",
            "services": ["Amazon VPC Lattice"],
            "config_rules": ["SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED"],
            "security_hub_controls": ["EC2.15"],
            "control_tower_ids": ["AWS-GR_SUBNET_AUTO_ASSIGN_PUBLIC_IP_DISABLED", "SH.EC2.15"],
            "frameworks": ["ISO-IEC-27001:2013-Annex-A", "PCI-DSS-v4.0"]
        },
        {
            "control_id": "AWS-CG-0000042",
            "title": "Restrict security group public Internet ingress traffic sources for remote access services",
            "description": "Prevent unauthorized access to EC2 resources by configuring security groups to restrict public Internet ingress traffic sources for remote access services.",
            "services": ["Amazon EC2"],
            "config_rules": ["INCOMING_SSH_DISABLED"],
            "security_hub_controls": ["EC2.13"],
            "control_tower_ids": ["AWS-GR_RESTRICTED_SSH"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
        },
        {
            "control_id": "AWS-CG-0000155",
            "title": "Remove unused Amazon EC2 security groups",
            "description": "Review and remove unused EC2 security groups to reduce complexity in network management and improve network security.",
            "services": ["Amazon EC2"],
            "config_rules": ["EC2_SECURITY_GROUP_ATTACHED_TO_ENI", "EC2_SECURITY_GROUP_ATTACHED_TO_ENI_PERIODIC"],
            "security_hub_controls": ["EC2.22"],
            "control_tower_ids": ["CONFIG.EC2.DT.11", "SH.EC2.22"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
        }
    ]
    
    # AC-17: Remote Access (VPN, Session Manager, Public Access Controls)
    data['controls']['ac-17'] = [
        {
            "control_id": "AWS-CG-0000224",
            "title": "Disable public access to Amazon EKS endpoints",
            "description": "Disable public access to Amazon EKS endpoints to avoid unintentional exposure and access to the cluster.",
            "services": ["Amazon Elastic Kubernetes Service"],
            "config_rules": ["EKS_ENDPOINT_NO_PUBLIC_ACCESS"],
            "security_hub_controls": ["EKS.1"],
            "control_tower_ids": ["AWS-GR_EKS_ENDPOINT_NO_PUBLIC_ACCESS", "SH.EKS.1"],
            "frameworks": ["ISO-IEC-27001:2013-Annex-A", "PCI-DSS-v4.0"]
        },
        {
            "control_id": "AWS-CG-0000198",
            "title": "Block public access to Amazon S3 buckets",
            "description": "Configure Amazon S3 to block public access to S3 buckets to protect data from unauthorized access.",
            "services": ["Amazon S3"],
            "config_rules": ["S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS", "S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC", "S3_BUCKET_LEVEL_PUBLIC_ACCESS_PROHIBITED", "S3_BUCKET_PUBLIC_READ_PROHIBITED", "S3_BUCKET_PUBLIC_WRITE_PROHIBITED"],
            "security_hub_controls": ["S3.1", "S3.2", "S3.3", "S3.8"],
            "control_tower_ids": ["AWS-GR_S3_ACCOUNT_LEVEL_PUBLIC_ACCESS_BLOCKS_PERIODIC", "AWS-GR_S3_BUCKET_PUBLIC_READ_PROHIBITED", "AWS-GR_S3_BUCKET_PUBLIC_WRITE_PROHIBITED", "CT.S3.PR.1", "SH.S3.1", "SH.S3.2", "SH.S3.3", "SH.S3.8"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0"]
        },
        {
            "control_id": "AWS-CG-0000174",
            "title": "Disable direct internet access for Amazon SageMaker Notebook instance",
            "description": "Restrict SageMaker Notebook instances from having direct internet access to avoid potential unauthorized access and data exposure.",
            "services": ["Amazon SageMaker"],
            "config_rules": ["SAGEMAKER_NOTEBOOK_NO_DIRECT_INTERNET_ACCESS"],
            "security_hub_controls": ["SageMaker.1"],
            "control_tower_ids": ["AWS-GR_SAGEMAKER_NOTEBOOK_NO_DIRECT_INTERNET_ACCESS", "SH.SageMaker.1"],
            "frameworks": ["ISO-IEC-27001:2013-Annex-A", "PCI-DSS-v4.0"]
        }
    ]
    
    # IR-8: Incident Response Plan (Security Hub, Backup, Monitoring)
    data['controls']['ir-8'] = [
        {
            "control_id": "AWS-CG-0000169",
            "title": "Enable AWS Security Hub service",
            "description": "Activate Security Hub in the AWS management console and configure the service to receive findings from supported AWS security services.",
            "services": ["AWS Security Hub"],
            "config_rules": ["SECURITYHUB_ENABLED"],
            "security_hub_controls": [],
            "control_tower_ids": ["CONFIG.SECURITYHUB.DT.1"],
            "frameworks": ["NIST-SP-800-53-r5", "PCI-DSS-v4.0", "SSAE-18-SOC-2-Oct-2023"]
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
            "control_id": "AWS-CG-0000108",
            "title": "Create access policies for backup vaults in AWS Backup",
            "description": "Create access policies for backup vaults in AWS Backup to prevent deletion of recovery point backups stored in the backup vault.",
            "services": ["AWS Backup"],
            "config_rules": ["BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED"],
            "security_hub_controls": [],
            "control_tower_ids": ["BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED"],
            "frameworks": ["NIST-SP-800-53-r5"]
        }
    ]
    
    # CP-2: Contingency Plan (Backup, Multi-region, DR)
    data['controls']['cp-2'] = [
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
            "description": "Configure recovery points for AWS Backup such that they do not expire before the retention period to prevent data loss and meet retention requirements.",
            "services": ["AWS Backup"],
            "config_rules": ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"],
            "security_hub_controls": [],
            "control_tower_ids": ["BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK"],
            "frameworks": []
        },
        {
            "control_id": "AWS-CG-0000220",
            "title": "Enable a backup plan for Amazon Elastic File System (EFS)",
            "description": "Enable a backup plan for Amazon EFS to ensure that data is regularly backed up.",
            "services": ["Amazon Elastic File System"],
            "config_rules": ["EFS_IN_BACKUP_PLAN", "EFS_RESOURCES_PROTECTED_BY_BACKUP_PLAN"],
            "security_hub_controls": ["EFS.2"],
            "control_tower_ids": ["CONFIG.ELASTICFILESYSTEM.DT.4", "CT.ELASTICFILESYSYSTEM.PR.2", "SH.EFS.2"],
            "frameworks": ["NIST-SP-800-53-r5"]
        }
    ]
    
    # CP-4: Contingency Plan Testing (Backup verification, Recovery testing)
    data['controls']['cp-4'] = [
        {
            "control_id": "AWS-CG-0000359",
            "title": "Ensure backup recovery points exists for Amazon Aurora",
            "description": "Ensure backup recovery points exists for Amazon Aurora to enable restoration.",
            "services": ["Amazon RDS"],
            "config_rules": ["AURORA_LAST_BACKUP_RECOVERY_POINT_CREATED"],
            "security_hub_controls": [],
            "control_tower_ids": ["AURORA_LAST_BACKUP_RECOVERY_POINT_CREATED"],
            "frameworks": ["NIST-SP-800-53-r5"]
        },
        {
            "control_id": "AWS-CG-0000641",
            "title": "Ensure regular recovery points for AWS Backup-Gateway virtual machines",
            "description": "Configure regular creation of recovery points for AWS Backup-Gateway virtual machines for protection and disaster recovery purposes.",
            "services": ["AWS Backup"],
            "config_rules": ["VIRTUALMACHINE_LAST_BACKUP_RECOVERY_POINT_CREATED"],
            "security_hub_controls": [],
            "control_tower_ids": ["CONFIG.BACKUP-GATEWAY.DT.3"],
            "frameworks": ["NIST-SP-800-53-r5", "SSAE-18-SOC-2-Oct-2023"]
        },
        {
            "control_id": "AWS-CG-0000108",
            "title": "Create access policies for backup vaults in AWS Backup",
            "description": "Create access policies for backup vaults in AWS Backup to prevent deletion of recovery point backups stored in the backup vault.",
            "services": ["AWS Backup"],
            "config_rules": ["BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED"],
            "security_hub_controls": [],
            "control_tower_ids": ["BACKUP_RECOVERY_POINT_MANUAL_DELETION_DISABLED"],
            "frameworks": ["NIST-SP-800-53-r5"]
        }
    ]
    
    # Update metadata
    data['metadata']['total_controls_mapped'] = len(data['controls'])
    data['metadata']['export_date'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # Save updated data
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Added 6 final controls:")
    print(f"  ✓ AU-9: Protection of Audit Information (3 AWS controls)")
    print(f"  ✓ CM-7: Least Functionality (3 AWS controls)")
    print(f"  ✓ AC-17: Remote Access (3 AWS controls)")
    print(f"  ✓ IR-8: Incident Response Plan (3 AWS controls)")
    print(f"  ✓ CP-2: Contingency Plan (3 AWS controls)")
    print(f"  ✓ CP-4: Contingency Plan Testing (3 AWS controls)")
    print(f"\nTotal controls in file: {data['metadata']['total_controls_mapped']}")
    print(f"\n🎉 ALL HIGH-PRIORITY CONTROLS COMPLETE! 🎉")
    print(f"Data saved to: {data_file}")


if __name__ == '__main__':
    main()

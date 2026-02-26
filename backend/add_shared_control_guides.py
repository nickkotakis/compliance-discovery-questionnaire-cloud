#!/usr/bin/env python3
"""Add AWS implementation guides for the 14 missing Shared controls."""

import json
import os

# AWS implementation guides for Shared controls
SHARED_CONTROL_GUIDES = {
    "ac-4": [
        {
            "control_id": "AWS-CG-AC-4-01",
            "title": "Implement network segmentation with VPC and Security Groups",
            "description": "Use Amazon VPC to create isolated network segments and Security Groups to control traffic flow between resources",
            "services": ["Amazon VPC", "Security Groups", "Network ACLs", "AWS Transit Gateway"],
            "config_rules": [
                "vpc-sg-open-only-to-authorized-ports",
                "vpc-default-security-group-closed",
                "restricted-ssh",
                "restricted-common-ports"
            ],
            "security_hub_controls": ["EC2.2", "EC2.13", "EC2.14", "EC2.21"],
            "control_tower_ids": ["CT.EC2.PR.1", "CT.EC2.PR.3"],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-AC-4-02",
            "title": "Use AWS Network Firewall for stateful traffic inspection",
            "description": "Deploy AWS Network Firewall to inspect and filter traffic between VPCs and to/from the internet",
            "services": ["AWS Network Firewall", "AWS Firewall Manager"],
            "config_rules": ["netfw-policy-rule-group-associated", "netfw-stateless-rule-group-not-empty"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-AC-4-03",
            "title": "Implement VPC Flow Logs for traffic monitoring",
            "description": "Enable VPC Flow Logs to capture information about IP traffic going to and from network interfaces",
            "services": ["VPC Flow Logs", "Amazon CloudWatch Logs"],
            "config_rules": ["vpc-flow-logs-enabled"],
            "security_hub_controls": ["EC2.6"],
            "control_tower_ids": ["CT.EC2.PR.14"],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA"]
        }
    ],
    "au-11": [
        {
            "control_id": "AWS-CG-AU-11-01",
            "title": "Configure S3 bucket lifecycle policies for log retention",
            "description": "Use S3 lifecycle policies to automatically transition and expire log files based on retention requirements",
            "services": ["Amazon S3", "S3 Lifecycle", "S3 Glacier"],
            "config_rules": ["s3-lifecycle-policy-check"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA", "SOX"]
        },
        {
            "control_id": "AWS-CG-AU-11-02",
            "title": "Enable S3 Object Lock for immutable audit logs",
            "description": "Use S3 Object Lock in compliance mode to prevent deletion or modification of audit logs during retention period",
            "services": ["Amazon S3", "S3 Object Lock"],
            "config_rules": ["s3-bucket-versioning-enabled"],
            "security_hub_controls": ["S3.14"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "SEC Rule 17a-4", "FINRA"]
        },
        {
            "control_id": "AWS-CG-AU-11-03",
            "title": "Use AWS Backup for long-term audit log retention",
            "description": "Configure AWS Backup to create and manage backups of audit logs with defined retention policies",
            "services": ["AWS Backup", "Amazon S3"],
            "config_rules": ["backup-plan-min-frequency-and-min-retention-check"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "HIPAA"]
        }
    ],
    "au-12": [
        {
            "control_id": "AWS-CG-AU-12-01",
            "title": "Enable CloudTrail for comprehensive audit logging",
            "description": "Configure AWS CloudTrail to log all API calls and management events across your AWS account",
            "services": ["AWS CloudTrail", "Amazon S3", "CloudWatch Logs"],
            "config_rules": [
                "cloud-trail-enabled",
                "cloud-trail-log-file-validation-enabled",
                "multi-region-cloud-trail-enabled"
            ],
            "security_hub_controls": ["CloudTrail.1", "CloudTrail.2", "CloudTrail.4"],
            "control_tower_ids": ["CT.CLOUDTRAIL.PR.1", "CT.CLOUDTRAIL.PR.2"],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA", "SOX"]
        },
        {
            "control_id": "AWS-CG-AU-12-02",
            "title": "Configure VPC Flow Logs for network traffic auditing",
            "description": "Enable VPC Flow Logs to capture detailed information about network traffic for security analysis",
            "services": ["VPC Flow Logs", "Amazon CloudWatch Logs", "Amazon S3"],
            "config_rules": ["vpc-flow-logs-enabled"],
            "security_hub_controls": ["EC2.6"],
            "control_tower_ids": ["CT.EC2.PR.14"],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-AU-12-03",
            "title": "Enable AWS Config for resource configuration auditing",
            "description": "Use AWS Config to record configuration changes and evaluate compliance against desired configurations",
            "services": ["AWS Config", "Amazon S3"],
            "config_rules": ["config-enabled"],
            "security_hub_controls": [],
            "control_tower_ids": ["CT.CONFIG.PR.1"],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA"]
        }
    ],
    "au-4": [
        {
            "control_id": "AWS-CG-AU-4-01",
            "title": "Configure CloudWatch Logs with sufficient retention",
            "description": "Set appropriate retention periods for CloudWatch Log Groups to ensure adequate storage capacity",
            "services": ["Amazon CloudWatch Logs", "Amazon S3"],
            "config_rules": ["cloudwatch-log-group-retention-period-check"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-AU-4-02",
            "title": "Use S3 for scalable audit log storage",
            "description": "Store audit logs in Amazon S3 for virtually unlimited storage capacity with automatic scaling",
            "services": ["Amazon S3", "S3 Intelligent-Tiering"],
            "config_rules": ["s3-bucket-versioning-enabled"],
            "security_hub_controls": ["S3.1"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-AU-4-03",
            "title": "Set up CloudWatch alarms for log storage capacity",
            "description": "Create CloudWatch alarms to monitor S3 bucket size and CloudWatch Logs storage to prevent capacity issues",
            "services": ["Amazon CloudWatch", "Amazon SNS"],
            "config_rules": ["cloudwatch-alarm-action-check"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "cm-6": [
        {
            "control_id": "AWS-CG-CM-6-01",
            "title": "Use AWS Config Rules for configuration compliance",
            "description": "Deploy AWS Config managed and custom rules to continuously evaluate resource configurations against security baselines",
            "services": ["AWS Config", "AWS Config Rules", "AWS Systems Manager"],
            "config_rules": [
                "approved-amis-by-id",
                "ec2-instance-managed-by-systems-manager",
                "encrypted-volumes",
                "required-tags"
            ],
            "security_hub_controls": ["Config.1"],
            "control_tower_ids": ["CT.CONFIG.PR.1"],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-CM-6-02",
            "title": "Implement AWS Systems Manager for configuration management",
            "description": "Use Systems Manager State Manager to define and maintain consistent configuration across EC2 instances",
            "services": ["AWS Systems Manager", "State Manager", "Parameter Store"],
            "config_rules": ["ec2-instance-managed-by-systems-manager"],
            "security_hub_controls": ["SSM.1", "SSM.2"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-CM-6-03",
            "title": "Use AWS Service Catalog for standardized configurations",
            "description": "Deploy AWS Service Catalog to provide pre-approved, standardized resource configurations",
            "services": ["AWS Service Catalog", "AWS CloudFormation"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "cp-10": [
        {
            "control_id": "AWS-CG-CP-10-01",
            "title": "Use AWS Backup for automated recovery",
            "description": "Configure AWS Backup to create recovery points and automate restoration of resources",
            "services": ["AWS Backup", "Amazon EBS", "Amazon RDS", "Amazon DynamoDB"],
            "config_rules": [
                "backup-plan-min-frequency-and-min-retention-check",
                "backup-recovery-point-encrypted",
                "backup-recovery-point-minimum-retention-check"
            ],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-CP-10-02",
            "title": "Implement automated disaster recovery with AWS Elastic Disaster Recovery",
            "description": "Use AWS Elastic Disaster Recovery (DRS) for automated failover and recovery of applications",
            "services": ["AWS Elastic Disaster Recovery", "Amazon EC2"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        },
        {
            "control_id": "AWS-CG-CP-10-03",
            "title": "Use CloudFormation for infrastructure reconstitution",
            "description": "Maintain CloudFormation templates to quickly reconstitute infrastructure in recovery scenarios",
            "services": ["AWS CloudFormation", "AWS CloudFormation StackSets"],
            "config_rules": ["cloudformation-stack-drift-detection-check"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "cp-6": [
        {
            "control_id": "AWS-CG-CP-6-01",
            "title": "Configure S3 Cross-Region Replication for alternate storage",
            "description": "Use S3 Cross-Region Replication to maintain copies of data in geographically separate regions",
            "services": ["Amazon S3", "S3 Replication"],
            "config_rules": ["s3-bucket-replication-enabled"],
            "security_hub_controls": ["S3.9"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-CP-6-02",
            "title": "Use AWS Backup for cross-region backup copies",
            "description": "Configure AWS Backup to automatically copy backups to alternate regions",
            "services": ["AWS Backup", "Amazon S3"],
            "config_rules": ["backup-recovery-point-encrypted"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-CP-6-03",
            "title": "Implement RDS automated backups with cross-region copies",
            "description": "Enable automated backups for RDS and configure cross-region snapshot copies",
            "services": ["Amazon RDS", "RDS Automated Backups"],
            "config_rules": ["rds-automatic-minor-version-upgrade-enabled", "db-backup-enabled"],
            "security_hub_controls": ["RDS.1"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        }
    ],
    "cp-7": [
        {
            "control_id": "AWS-CG-CP-7-01",
            "title": "Deploy multi-region architecture for alternate processing",
            "description": "Use multiple AWS regions to maintain alternate processing sites with automated failover capabilities",
            "services": ["Amazon Route 53", "AWS Global Accelerator", "Amazon CloudFront"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-CP-7-02",
            "title": "Use AWS Elastic Disaster Recovery for alternate site",
            "description": "Configure AWS Elastic Disaster Recovery to maintain a ready alternate processing site",
            "services": ["AWS Elastic Disaster Recovery", "Amazon EC2"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        },
        {
            "control_id": "AWS-CG-CP-7-03",
            "title": "Implement Auto Scaling for rapid capacity provisioning",
            "description": "Use Auto Scaling groups to quickly provision processing capacity in alternate regions",
            "services": ["Amazon EC2 Auto Scaling", "Application Auto Scaling"],
            "config_rules": ["autoscaling-group-elb-healthcheck-required"],
            "security_hub_controls": ["AutoScaling.1"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "ia-3": [
        {
            "control_id": "AWS-CG-IA-3-01",
            "title": "Use AWS IoT Device Defender for device authentication",
            "description": "Implement AWS IoT Device Defender to authenticate and authorize IoT devices",
            "services": ["AWS IoT Core", "AWS IoT Device Defender"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        },
        {
            "control_id": "AWS-CG-IA-3-02",
            "title": "Implement certificate-based authentication for devices",
            "description": "Use AWS Certificate Manager and IoT Core certificates for device authentication",
            "services": ["AWS Certificate Manager", "AWS IoT Core"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-IA-3-03",
            "title": "Use VPC endpoints for private device connectivity",
            "description": "Configure VPC endpoints to ensure devices connect through private network paths",
            "services": ["Amazon VPC", "VPC Endpoints"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "ia-4": [
        {
            "control_id": "AWS-CG-IA-4-01",
            "title": "Implement IAM user naming conventions and tagging",
            "description": "Use consistent naming conventions and tags for IAM users to manage identifiers effectively",
            "services": ["AWS IAM", "AWS Organizations"],
            "config_rules": ["iam-user-unused-credentials-check", "required-tags"],
            "security_hub_controls": ["IAM.4"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-IA-4-02",
            "title": "Use AWS SSO for centralized identifier management",
            "description": "Implement AWS IAM Identity Center (SSO) to centrally manage user identifiers across AWS accounts",
            "services": ["AWS IAM Identity Center", "AWS Organizations"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        },
        {
            "control_id": "AWS-CG-IA-4-03",
            "title": "Automate user provisioning with SCIM",
            "description": "Use SCIM (System for Cross-domain Identity Management) to automate user identifier provisioning",
            "services": ["AWS IAM Identity Center", "SCIM"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "ia-8": [
        {
            "control_id": "AWS-CG-IA-8-01",
            "title": "Use IAM Identity Center for federated access",
            "description": "Configure AWS IAM Identity Center to authenticate non-organizational users through external identity providers",
            "services": ["AWS IAM Identity Center", "SAML 2.0", "OpenID Connect"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "FedRAMP"]
        },
        {
            "control_id": "AWS-CG-IA-8-02",
            "title": "Implement Amazon Cognito for external user authentication",
            "description": "Use Amazon Cognito to authenticate and authorize external users accessing applications",
            "services": ["Amazon Cognito", "Cognito User Pools", "Cognito Identity Pools"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        },
        {
            "control_id": "AWS-CG-IA-8-03",
            "title": "Configure cross-account access with IAM roles",
            "description": "Use IAM roles and trust policies to authenticate users from external AWS accounts",
            "services": ["AWS IAM", "IAM Roles", "AWS STS"],
            "config_rules": ["iam-role-managed-policy-check"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "ir-5": [
        {
            "control_id": "AWS-CG-IR-5-01",
            "title": "Use Amazon GuardDuty for threat detection and monitoring",
            "description": "Enable GuardDuty to continuously monitor for malicious activity and unauthorized behavior",
            "services": ["Amazon GuardDuty", "AWS Security Hub"],
            "config_rules": ["guardduty-enabled-centralized"],
            "security_hub_controls": ["GuardDuty.1"],
            "control_tower_ids": ["CT.GUARDDUTY.PR.1"],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-IR-5-02",
            "title": "Implement AWS Security Hub for centralized monitoring",
            "description": "Use Security Hub to aggregate and monitor security findings from multiple AWS services",
            "services": ["AWS Security Hub", "Amazon EventBridge"],
            "config_rules": ["securityhub-enabled"],
            "security_hub_controls": [],
            "control_tower_ids": ["CT.SECURITYHUB.PR.1"],
            "frameworks": ["NIST 800-53", "PCI-DSS", "HIPAA"]
        },
        {
            "control_id": "AWS-CG-IR-5-03",
            "title": "Configure CloudWatch Logs Insights for incident analysis",
            "description": "Use CloudWatch Logs Insights to query and analyze log data for incident detection",
            "services": ["Amazon CloudWatch Logs", "CloudWatch Logs Insights"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "ir-6": [
        {
            "control_id": "AWS-CG-IR-6-01",
            "title": "Use AWS Security Hub for automated incident reporting",
            "description": "Configure Security Hub to automatically send findings to incident management systems",
            "services": ["AWS Security Hub", "Amazon EventBridge", "Amazon SNS"],
            "config_rules": ["securityhub-enabled"],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-IR-6-02",
            "title": "Configure GuardDuty notifications for security incidents",
            "description": "Set up GuardDuty to send notifications to security teams when threats are detected",
            "services": ["Amazon GuardDuty", "Amazon SNS", "Amazon EventBridge"],
            "config_rules": ["guardduty-enabled-centralized"],
            "security_hub_controls": ["GuardDuty.1"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-IR-6-03",
            "title": "Implement AWS Systems Manager Incident Manager",
            "description": "Use Systems Manager Incident Manager to track and manage incident response activities",
            "services": ["AWS Systems Manager Incident Manager", "Amazon SNS"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        }
    ],
    "si-7": [
        {
            "control_id": "AWS-CG-SI-7-01",
            "title": "Use Amazon Inspector for software integrity scanning",
            "description": "Enable Amazon Inspector to continuously scan for software vulnerabilities and integrity issues",
            "services": ["Amazon Inspector", "AWS Security Hub"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        },
        {
            "control_id": "AWS-CG-SI-7-02",
            "title": "Implement AWS Signer for code signing",
            "description": "Use AWS Signer to digitally sign code and verify software integrity",
            "services": ["AWS Signer", "AWS Lambda"],
            "config_rules": [],
            "security_hub_controls": [],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53"]
        },
        {
            "control_id": "AWS-CG-SI-7-03",
            "title": "Enable EC2 Instance Metadata Service v2 (IMDSv2)",
            "description": "Use IMDSv2 to protect instance metadata from unauthorized access and ensure integrity",
            "services": ["Amazon EC2", "EC2 Instance Metadata Service"],
            "config_rules": ["ec2-imdsv2-check"],
            "security_hub_controls": ["EC2.8"],
            "control_tower_ids": [],
            "frameworks": ["NIST 800-53", "PCI-DSS"]
        }
    ]
}


def main():
    """Add AWS implementation guides for Shared controls."""
    
    # Load existing MCP data
    mcp_file = 'compliance_discovery/aws_controls_mcp_data.json'
    
    if os.path.exists(mcp_file):
        with open(mcp_file, 'r') as f:
            data = json.load(f)
    else:
        data = {
            "metadata": {
                "version": "1.0.0",
                "last_updated": "2026-02-26",
                "source": "AWS Control Compass and manual curation"
            },
            "controls": {}
        }
    
    # Add new controls
    controls_added = 0
    for control_id, guides in SHARED_CONTROL_GUIDES.items():
        if control_id not in data['controls']:
            data['controls'][control_id] = guides
            controls_added += 1
            print(f"Added {len(guides)} implementation guides for {control_id.upper()}")
        else:
            print(f"Skipping {control_id.upper()} - already has guides")
    
    # Update metadata
    data['metadata']['last_updated'] = '2026-02-26'
    data['metadata']['total_controls'] = len(data['controls'])
    
    # Save updated data
    with open(mcp_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Successfully added implementation guides for {controls_added} Shared controls")
    print(f"Total controls with guides: {len(data['controls'])}")
    print(f"\nUpdated file: {mcp_file}")


if __name__ == '__main__':
    main()

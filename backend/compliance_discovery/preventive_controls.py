"""Preventive controls data for SCPs and OPA/Rego policies.

SCPs (Service Control Policies) are preventive guardrails enforced at the
AWS Organizations level. They prevent actions from ever happening, regardless
of IAM permissions.

OPA (Open Policy Agent) Rego policies validate Terraform/CloudFormation
templates before deployment, catching misconfigurations in the CI/CD pipeline.

Both complement the detective controls (Config Rules, Security Hub) already
in the implementation guides.

AWS Service mapping:
- SCPs → AWS Organizations (preventive, account-level)
- OPA/Rego → CI/CD Pipeline / Terraform (preventive, pre-deployment)
- Config Rules → AWS Config (detective, continuous)
- Security Hub → AWS 
Security Hub (detective, continuous)
- Control Tower → AWS Control Tower (preventive + detective)
"""

from typing import Dict, List, Optional, Any


# =========================================================================
# SCP (Service Control Policy) recommendations by control family
# These are well-known SCPs that map to compliance control families.
# Service: AWS Organizations
# Type: Preventive (blocks actions at the API level)
# =========================================================================

# Maps NIST 800-53 control families to relevant SCPs
NIST_800_53_SCPS: Dict[str, List[Dict[str, str]]] = {
    # AC — Access Control
    "AC": [
        {
            "scp_name": "Deny root account usage",
            "scp_id": "SCP-DenyRootAccount",
            "description": "Prevents use of the root user for any operations except those that require root credentials",
            "example_actions": "Deny: * (with condition aws:PrincipalArn matches root)"
        },
        {
            "scp_name": "Restrict IAM user creation",
            "scp_id": "SCP-RestrictIAMUserCreation",
            "description": "Prevents creation of IAM users with long-lived credentials, enforcing federation through IAM Identity Center",
            "example_actions": "Deny: iam:CreateUser, iam:CreateAccessKey"
        },
        {
            "scp_name": "Require MFA for sensitive actions",
            "scp_id": "SCP-RequireMFA",
            "description": "Denies sensitive actions unless MFA is present in the request context",
            "example_actions": "Deny: iam:DeactivateMFADevice, iam:DeleteVirtualMFADevice (without MFA)"
        },
        {
            "scp_name": "Deny access key creation for root",
            "scp_id": "SCP-DenyRootAccessKeys",
            "description": "Prevents creation of access keys for the root account",
            "example_actions": "Deny: iam:CreateAccessKey (for root principal)"
        },
    ],
    # AU — Audit and Accountability
    "AU": [
        {
            "scp_name": "Prevent CloudTrail modification",
            "scp_id": "SCP-ProtectCloudTrail",
            "description": "Prevents anyone from stopping, deleting, or modifying CloudTrail logging",
            "example_actions": "Deny: cloudtrail:StopLogging, cloudtrail:DeleteTrail, cloudtrail:UpdateTrail"
        },
        {
            "scp_name": "Protect CloudWatch Logs",
            "scp_id": "SCP-ProtectCloudWatchLogs",
            "description": "Prevents deletion of CloudWatch log groups used for audit logging",
            "example_actions": "Deny: logs:DeleteLogGroup, logs:DeleteLogStream"
        },
        {
            "scp_name": "Protect S3 audit log buckets",
            "scp_id": "SCP-ProtectAuditBuckets",
            "description": "Prevents deletion or modification of S3 buckets designated for audit log storage",
            "example_actions": "Deny: s3:DeleteBucket, s3:PutBucketPolicy (on audit buckets)"
        },
    ],
    # CM — Configuration Management
    "CM": [
        {
            "scp_name": "Restrict AWS Regions",
            "scp_id": "SCP-RestrictRegions",
            "description": "Limits resource creation to approved AWS Regions only, preventing shadow deployments in unauthorized regions",
            "example_actions": "Deny: * (where aws:RequestedRegion not in approved list)"
        },
        {
            "scp_name": "Prevent Config rule deletion",
            "scp_id": "SCP-ProtectConfigRules",
            "description": "Prevents deletion or modification of AWS Config rules and recorders",
            "example_actions": "Deny: config:DeleteConfigRule, config:StopConfigurationRecorder"
        },
        {
            "scp_name": "Restrict service usage",
            "scp_id": "SCP-RestrictServices",
            "description": "Limits which AWS services can be used, enforcing least functionality",
            "example_actions": "Deny: specific service actions not in approved service list"
        },
    ],
    # IA — Identification and Authentication
    "IA": [
        {
            "scp_name": "Enforce MFA for console access",
            "scp_id": "SCP-EnforceMFA",
            "description": "Denies all actions except identity-related ones unless MFA is authenticated",
            "example_actions": "Deny: * (without aws:MultiFactorAuthPresent condition)"
        },
    ],
    # IR — Incident Response
    "IR": [
        {
            "scp_name": "Protect GuardDuty configuration",
            "scp_id": "SCP-ProtectGuardDuty",
            "description": "Prevents disabling or modifying GuardDuty detectors used for threat detection",
            "example_actions": "Deny: guardduty:DeleteDetector, guardduty:DisassociateFromMasterAccount"
        },
    ],
    # SC — System and Communications Protection
    "SC": [
        {
            "scp_name": "Deny unencrypted S3 uploads",
            "scp_id": "SCP-DenyUnencryptedS3",
            "description": "Prevents uploading objects to S3 without server-side encryption",
            "example_actions": "Deny: s3:PutObject (without x-amz-server-side-encryption header)"
        },
        {
            "scp_name": "Deny public S3 access",
            "scp_id": "SCP-DenyPublicS3",
            "description": "Prevents making S3 buckets or objects publicly accessible",
            "example_actions": "Deny: s3:PutBucketPublicAccessBlock (if disabling), s3:PutBucketAcl (if public)"
        },
        {
            "scp_name": "Require TLS for data in transit",
            "scp_id": "SCP-RequireTLS",
            "description": "Denies API calls that don't use TLS, enforcing encryption in transit",
            "example_actions": "Deny: * (where aws:SecureTransport is false)"
        },
        {
            "scp_name": "Deny unencrypted EBS volumes",
            "scp_id": "SCP-DenyUnencryptedEBS",
            "description": "Prevents creation of unencrypted EBS volumes",
            "example_actions": "Deny: ec2:CreateVolume (without encryption)"
        },
        {
            "scp_name": "Deny unencrypted RDS instances",
            "scp_id": "SCP-DenyUnencryptedRDS",
            "description": "Prevents creation of unencrypted RDS database instances",
            "example_actions": "Deny: rds:CreateDBInstance (without StorageEncrypted)"
        },
        {
            "scp_name": "Restrict VPC modifications",
            "scp_id": "SCP-RestrictVPCChanges",
            "description": "Prevents unauthorized modifications to VPC configurations, internet gateways, and route tables",
            "example_actions": "Deny: ec2:CreateInternetGateway, ec2:AttachInternetGateway (without approval tag)"
        },
    ],
    # SI — System and Information Integrity
    "SI": [
        {
            "scp_name": "Protect Security Hub configuration",
            "scp_id": "SCP-ProtectSecurityHub",
            "description": "Prevents disabling Security Hub or removing member accounts",
            "example_actions": "Deny: securityhub:DisableSecurityHub, securityhub:DisassociateFromMasterAccount"
        },
        {
            "scp_name": "Protect Inspector configuration",
            "scp_id": "SCP-ProtectInspector",
            "description": "Prevents disabling Amazon Inspector scanning",
            "example_actions": "Deny: inspector2:Disable, inspector2:DisassociateMember"
        },
    ],
    # CP — Contingency Planning
    "CP": [
        {
            "scp_name": "Protect backup vaults",
            "scp_id": "SCP-ProtectBackups",
            "description": "Prevents deletion of AWS Backup vaults and recovery points",
            "example_actions": "Deny: backup:DeleteBackupVault, backup:DeleteRecoveryPoint"
        },
    ],
    # MP — Media Protection
    "MP": [
        {
            "scp_name": "Enforce S3 encryption at rest",
            "scp_id": "SCP-EnforceS3Encryption",
            "description": "Requires all S3 objects to be encrypted with KMS",
            "example_actions": "Deny: s3:PutObject (without aws:kms encryption)"
        },
    ],
    # RA — Risk Assessment
    "RA": [
        {
            "scp_name": "Protect vulnerability scanning",
            "scp_id": "SCP-ProtectScanning",
            "description": "Prevents disabling Amazon Inspector or modifying scan configurations",
            "example_actions": "Deny: inspector2:Disable, inspector2:UpdateOrganizationConfiguration"
        },
    ],
}


# =========================================================================
# OPA/Rego policy recommendations by control family
# These validate Terraform/IaC before deployment.
# Service: CI/CD Pipeline (Terraform, CloudFormation)
# Type: Preventive (blocks deployment of non-compliant resources)
# =========================================================================

NIST_800_53_OPA: Dict[str, List[Dict[str, str]]] = {
    "AC": [
        {
            "opa_rule": "IAM_POLICY_NO_WILDCARD_RESOURCES",
            "description": "Ensures IAM policies don't use wildcard (*) for resources without conditions",
            "resource_types": "aws_iam_policy, aws_iam_role_policy",
            "severity": "HIGH"
        },
        {
            "opa_rule": "IAM_NO_INLINE_POLICIES",
            "description": "Ensures IAM roles and users don't have inline policies (use managed policies instead)",
            "resource_types": "aws_iam_role, aws_iam_user",
            "severity": "MEDIUM"
        },
    ],
    "AU": [
        {
            "opa_rule": "CLOUDTRAIL_ENABLED_ALL_REGIONS",
            "description": "Validates CloudTrail is configured for all regions with log file validation",
            "resource_types": "aws_cloudtrail",
            "severity": "CRITICAL"
        },
        {
            "opa_rule": "CLOUDWATCH_LOG_GROUP_RETENTION",
            "description": "Ensures CloudWatch log groups have retention periods set (not indefinite)",
            "resource_types": "aws_cloudwatch_log_group",
            "severity": "MEDIUM"
        },
    ],
    "CM": [
        {
            "opa_rule": "REQUIRED_TAGS_CHECK",
            "description": "Validates all resources have required tags (environment, owner, data-classification)",
            "resource_types": "All taggable resources",
            "severity": "MEDIUM"
        },
        {
            "opa_rule": "APPROVED_AMI_CHECK",
            "description": "Ensures EC2 instances use only approved, hardened AMIs",
            "resource_types": "aws_instance, aws_launch_template",
            "severity": "HIGH"
        },
    ],
    "IA": [
        {
            "opa_rule": "IAM_MFA_REQUIRED",
            "description": "Validates IAM policies include MFA conditions for sensitive actions",
            "resource_types": "aws_iam_policy",
            "severity": "HIGH"
        },
        {
            "opa_rule": "SECRETS_NO_PLAINTEXT",
            "description": "Ensures no plaintext secrets in Terraform variables or resource configurations",
            "resource_types": "All resources",
            "severity": "CRITICAL"
        },
    ],
    "SC": [
        {
            "opa_rule": "S3_BUCKET_ENCRYPTION_ENABLED",
            "description": "Validates S3 buckets have server-side encryption configured with KMS",
            "resource_types": "aws_s3_bucket, aws_s3_bucket_server_side_encryption_configuration",
            "severity": "HIGH"
        },
        {
            "opa_rule": "S3_BUCKET_PUBLIC_ACCESS_BLOCKED",
            "description": "Ensures S3 buckets have public access block enabled",
            "resource_types": "aws_s3_bucket_public_access_block",
            "severity": "CRITICAL"
        },
        {
            "opa_rule": "EBS_VOLUME_ENCRYPTION",
            "description": "Validates all EBS volumes are encrypted",
            "resource_types": "aws_ebs_volume, aws_instance",
            "severity": "HIGH"
        },
        {
            "opa_rule": "RDS_ENCRYPTION_ENABLED",
            "description": "Ensures RDS instances have storage encryption enabled",
            "resource_types": "aws_db_instance, aws_rds_cluster",
            "severity": "HIGH"
        },
        {
            "opa_rule": "SECURITY_GROUP_NO_UNRESTRICTED_INGRESS",
            "description": "Prevents security groups with 0.0.0.0/0 ingress on sensitive ports (SSH, RDP, DB)",
            "resource_types": "aws_security_group, aws_security_group_rule",
            "severity": "CRITICAL"
        },
        {
            "opa_rule": "VPC_FLOW_LOGS_ENABLED",
            "description": "Validates VPCs have flow logs enabled for network monitoring",
            "resource_types": "aws_vpc, aws_flow_log",
            "severity": "HIGH"
        },
        {
            "opa_rule": "ALB_HTTPS_ONLY",
            "description": "Ensures ALB listeners use HTTPS with TLS 1.2+",
            "resource_types": "aws_lb_listener",
            "severity": "HIGH"
        },
    ],
    "SI": [
        {
            "opa_rule": "GUARDDUTY_ENABLED",
            "description": "Validates GuardDuty detector is enabled in the account",
            "resource_types": "aws_guardduty_detector",
            "severity": "HIGH"
        },
        {
            "opa_rule": "SSM_PATCH_COMPLIANCE",
            "description": "Ensures Systems Manager patch baselines are configured for EC2 instances",
            "resource_types": "aws_ssm_patch_baseline, aws_ssm_patch_group",
            "severity": "MEDIUM"
        },
    ],
    "CP": [
        {
            "opa_rule": "BACKUP_PLAN_EXISTS",
            "description": "Validates AWS Backup plans exist for critical resources",
            "resource_types": "aws_backup_plan, aws_backup_selection",
            "severity": "HIGH"
        },
        {
            "opa_rule": "RDS_MULTI_AZ",
            "description": "Ensures production RDS instances are configured for Multi-AZ",
            "resource_types": "aws_db_instance",
            "severity": "HIGH"
        },
    ],
    "MP": [
        {
            "opa_rule": "S3_DEFAULT_ENCRYPTION_KMS",
            "description": "Validates S3 buckets use KMS encryption (not just AES-256)",
            "resource_types": "aws_s3_bucket_server_side_encryption_configuration",
            "severity": "HIGH"
        },
    ],
    "RA": [
        {
            "opa_rule": "INSPECTOR_ENABLED",
            "description": "Validates Amazon Inspector is enabled for vulnerability scanning",
            "resource_types": "aws_inspector2_enabler",
            "severity": "HIGH"
        },
    ],
}


# =========================================================================
# Mapping from NIST 800-53 families to CSF functions/categories
# Used to derive CSF and CMMC preventive controls from the 800-53 base
# =========================================================================

CSF_FUNCTION_TO_800_53_FAMILIES: Dict[str, List[str]] = {
    "GV": ["AC", "AU", "CM", "IA", "SC", "SI"],  # Govern — cross-cutting
    "ID": ["CM", "RA", "CP"],                      # Identify
    "PR": ["AC", "IA", "SC", "CM", "MP", "CP"],    # Protect
    "DE": ["AU", "SI", "IR"],                       # Detect
    "RS": ["IR", "SI"],                             # Respond
    "RC": ["CP", "IR"],                             # Recover
}

CMMC_DOMAIN_TO_800_53_FAMILIES: Dict[str, List[str]] = {
    "AC": ["AC"],
    "AT": [],       # Awareness — no direct SCP/OPA mapping
    "AU": ["AU"],
    "CM": ["CM"],
    "IA": ["IA"],
    "IR": ["IR"],
    "MA": [],       # Maintenance — mostly procedural
    "MP": ["MP", "SC"],
    "PE": [],       # Physical — no AWS SCP/OPA mapping
    "PS": [],       # Personnel — no AWS SCP/OPA mapping
    "RA": ["RA", "SI"],
    "CA": ["CM", "AU"],
    "SC": ["SC"],
    "SI": ["SI"],
}


def get_scps_for_control(control_id: str, framework: str = 'nist-800-53') -> List[Dict[str, str]]:
    """Get SCP recommendations for a control based on its family/domain.

    Args:
        control_id: Control ID (e.g., 'AC-2', 'PR.AA-01', 'AC.L2-3.1.1')
        framework: Framework identifier

    Returns:
        List of SCP recommendation dicts
    """
    families = _get_800_53_families(control_id, framework)
    scps = []
    seen = set()
    for fam in families:
        for scp in NIST_800_53_SCPS.get(fam, []):
            if scp['scp_id'] not in seen:
                seen.add(scp['scp_id'])
                scps.append(scp)
    return scps


def get_opa_rules_for_control(control_id: str, framework: str = 'nist-800-53') -> List[Dict[str, str]]:
    """Get OPA/Rego policy recommendations for a control.

    Args:
        control_id: Control ID
        framework: Framework identifier

    Returns:
        List of OPA rule recommendation dicts
    """
    families = _get_800_53_families(control_id, framework)
    rules = []
    seen = set()
    for fam in families:
        for rule in NIST_800_53_OPA.get(fam, []):
            if rule['opa_rule'] not in seen:
                seen.add(rule['opa_rule'])
                rules.append(rule)
    return rules


def get_preventive_controls_for_control(control_id: str, framework: str = 'nist-800-53') -> Dict[str, Any]:
    """Get all preventive control recommendations (SCPs + OPA) for a control.

    Args:
        control_id: Control ID
        framework: Framework identifier

    Returns:
        Dict with 'scps' and 'opa_rules' lists
    """
    return {
        'scps': get_scps_for_control(control_id, framework),
        'opa_rules': get_opa_rules_for_control(control_id, framework),
    }


def _get_800_53_families(control_id: str, framework: str) -> List[str]:
    """Map a control ID to NIST 800-53 families for SCP/OPA lookup.

    Args:
        control_id: Control ID from any framework
        framework: Framework identifier

    Returns:
        List of NIST 800-53 family codes
    """
    if framework == 'nist-800-53':
        # Extract family from control ID like "AC-2", "SC-7(3)"
        family = control_id.upper().split('-')[0]
        return [family]

    elif framework == 'nist-csf':
        # Extract function from CSF ID like "PR.AA-01", "DE.CM-06"
        function = control_id.upper().split('.')[0]
        return CSF_FUNCTION_TO_800_53_FAMILIES.get(function, [])

    elif framework == 'cmmc':
        # Extract domain from CMMC ID like "AC.L2-3.1.1"
        domain = control_id.upper().split('.')[0]
        return CMMC_DOMAIN_TO_800_53_FAMILIES.get(domain, [])

    return []


def get_control_type_label(control_data: Dict[str, Any]) -> str:
    """Determine if a control is preventive, detective, or both.

    Based on the types of managed controls present:
    - SCPs, Control Tower proactive controls → Preventive
    - Config Rules, Security Hub → Detective
    - OPA/Rego → Preventive (pre-deployment)

    Args:
        control_data: Dict with config_rules, security_hub_controls,
                      control_tower_ids, scps, opa_rules

    Returns:
        'preventive', 'detective', or 'both'
    """
    has_detective = bool(
        control_data.get('config_rules') or
        control_data.get('security_hub_controls')
    )
    has_preventive = bool(
        control_data.get('control_tower_ids') or
        control_data.get('scps') or
        control_data.get('opa_rules')
    )

    if has_preventive and has_detective:
        return 'both'
    elif has_preventive:
        return 'preventive'
    elif has_detective:
        return 'detective'
    return 'detective'  # default

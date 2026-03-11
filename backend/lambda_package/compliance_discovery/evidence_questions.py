"""NIST 800-53 family-level evidence question templates.

Provides specific, auditable evidence guidance for each control family,
replacing generic evidence questions with targeted artifact requests.
"""

from typing import Optional

# Family-level evidence templates keyed by family code.
# Each template is a dict with:
#   'policy': evidence question for -1 (policy/procedure) controls
#   'technical': evidence question template for technical controls
#   'keywords': dict mapping keyword patterns to specialized evidence questions
FAMILY_EVIDENCE_TEMPLATES = {
    'AC': {
        'policy': (
            "Provide: (1) Access control policy document with approval signatures and review history, "
            "(2) AWS Organizations SCP inventory enforcing access boundaries, "
            "(3) IAM permission boundary policy documents, "
            "(4) Evidence of annual policy review and update cycle."
        ),
        'technical': (
            "Provide: (1) IAM credential report showing MFA status, access key age, and last-used dates, "
            "(2) IAM Access Analyzer findings report identifying unused or excessive permissions, "
            "(3) AWS Config compliance reports for IAM-related rules (e.g., MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS, "
            "IAM_POLICY_NO_STATEMENTS_WITH_FULL_ACCESS), "
            "(4) CloudTrail logs showing access control enforcement events."
        ),
        'keywords': {
            'remote': (
                "Provide: (1) AWS Client VPN or Systems Manager Session Manager configuration evidence, "
                "(2) CloudTrail logs showing remote session activity, "
                "(3) Security group rules restricting remote access ports, "
                "(4) MFA enforcement evidence for remote access sessions."
            ),
            'separation': (
                "Provide: (1) IAM role separation matrix showing incompatible duties are in separate roles, "
                "(2) SCP policies preventing single-user privilege escalation, "
                "(3) AWS Organizations account structure showing environment separation."
            ),
            'session': (
                "Provide: (1) IAM role session duration configurations, "
                "(2) AWS SSO session timeout settings, "
                "(3) CloudTrail logs showing session activity and termination events."
            ),
        },
    },
    'AT': {
        'policy': (
            "Provide: (1) Security awareness and training policy with approval signatures, "
            "(2) Training curriculum covering AWS-specific security topics, "
            "(3) Annual training schedule and target audience definitions, "
            "(4) Policy review records showing updates for new AWS threats."
        ),
        'technical': (
            "Provide: (1) Training completion records with dates and pass rates by role, "
            "(2) AWS-specific training materials (IAM best practices, S3 security, CloudTrail), "
            "(3) Phishing simulation results and trend data, "
            "(4) Role-based training records for privileged AWS users."
        ),
        'keywords': {},
    },
    'AU': {
        'policy': (
            "Provide: (1) Audit and accountability policy with log retention requirements, "
            "(2) Logging standards document specifying which events must be captured, "
            "(3) Log review procedures and frequency requirements, "
            "(4) Evidence of policy approval and review cycle."
        ),
        'technical': (
            "Provide: (1) CloudTrail configuration showing multi-region trail with management and data events enabled, "
            "(2) CloudWatch Logs retention policy configurations, "
            "(3) S3 access logging and VPC Flow Log configurations, "
            "(4) Centralized logging architecture evidence (e.g., logging account with S3 Object Lock), "
            "(5) Log analysis tool configurations (CloudWatch Insights queries, Athena queries, or SIEM integration)."
        ),
        'keywords': {
            'review': (
                "Provide: (1) Scheduled CloudWatch Insights or Athena queries for log review, "
                "(2) Security Hub automated finding generation from log analysis, "
                "(3) Log review assignment records and findings documentation."
            ),
            'retention': (
                "Provide: (1) S3 lifecycle policies for CloudTrail log buckets, "
                "(2) CloudWatch Logs retention period configurations, "
                "(3) Glacier or S3 Glacier Deep Archive transition rules for long-term retention."
            ),
            'protection': (
                "Provide: (1) S3 Object Lock configuration on CloudTrail log buckets, "
                "(2) KMS key policies for log encryption, "
                "(3) IAM policies restricting log deletion access, "
                "(4) CloudTrail log file integrity validation configuration."
            ),
        },
    },
    'CA': {
        'policy': (
            "Provide: (1) Security assessment and authorization policy document, "
            "(2) Assessment methodology documentation (frequency, scope, approach), "
            "(3) Plan of Action and Milestones (POA&M) management procedures, "
            "(4) Authorization to Operate (ATO) documentation."
        ),
        'technical': (
            "Provide: (1) AWS Audit Manager assessment results and evidence folders, "
            "(2) Security Hub compliance standard scores (CIS, FSBP, PCI DSS), "
            "(3) AWS Config conformance pack compliance reports, "
            "(4) Penetration test reports for AWS workloads (per AWS pen test policy), "
            "(5) POA&M tracking records with remediation timelines."
        ),
        'keywords': {
            'continuous': (
                "Provide: (1) Security Hub continuous monitoring dashboard configuration, "
                "(2) AWS Config rule evaluation frequency settings, "
                "(3) GuardDuty continuous threat detection configuration, "
                "(4) Automated compliance reporting schedules."
            ),
        },
    },
    'CM': {
        'policy': (
            "Provide: (1) Configuration management policy with baseline requirements, "
            "(2) Change management procedures including security impact analysis steps, "
            "(3) Approved configuration baseline documents for each system type, "
            "(4) Policy review and approval records."
        ),
        'technical': (
            "Provide: (1) AWS Config rule compliance reports for configuration baselines, "
            "(2) CloudFormation or CDK templates defining approved configurations, "
            "(3) AWS Config configuration recorder settings showing all resource types monitored, "
            "(4) Systems Manager State Manager association compliance reports, "
            "(5) Change management ticket records showing security review before approval."
        ),
        'keywords': {
            'baseline': (
                "Provide: (1) AWS Config conformance pack results for CIS or custom baselines, "
                "(2) EC2 Image Builder hardened AMI configurations, "
                "(3) Systems Manager State Manager baseline association documents."
            ),
            'change': (
                "Provide: (1) Change management ticket records with security impact analysis, "
                "(2) CloudFormation change set reviews before deployment, "
                "(3) AWS Config drift detection reports, "
                "(4) CloudTrail logs showing configuration change events."
            ),
            'inventory': (
                "Provide: (1) AWS Config resource inventory reports, "
                "(2) Systems Manager Inventory reports for EC2 instances, "
                "(3) Software inventory from SSM showing installed applications and versions."
            ),
        },
    },
    'CP': {
        'policy': (
            "Provide: (1) Contingency planning policy with RTO/RPO requirements, "
            "(2) Business impact analysis (BIA) document, "
            "(3) Contingency plan document with AWS-specific recovery procedures, "
            "(4) Plan testing schedule and approval records."
        ),
        'technical': (
            "Provide: (1) AWS Backup policy configurations with retention periods and cross-Region replication, "
            "(2) Backup restoration test records with dates and results, "
            "(3) Multi-AZ and Multi-Region deployment configurations, "
            "(4) Route 53 health check and failover routing configurations, "
            "(5) Disaster recovery exercise records (AWS Fault Injection Service results or tabletop exercises)."
        ),
        'keywords': {
            'backup': (
                "Provide: (1) AWS Backup vault configurations and backup plans, "
                "(2) Backup Vault Lock configuration evidence, "
                "(3) Backup restoration test records with success/failure results, "
                "(4) KMS key configuration for backup encryption."
            ),
            'recovery': (
                "Provide: (1) DR runbook with step-by-step AWS recovery procedures, "
                "(2) CloudFormation/CDK templates for infrastructure redeployment, "
                "(3) DR test records showing RTO/RPO achievement, "
                "(4) Cross-Region replication configurations."
            ),
        },
    },
    'IA': {
        'policy': (
            "Provide: (1) Identification and authentication policy document, "
            "(2) Password/credential complexity and rotation requirements, "
            "(3) MFA enforcement policy for all AWS access, "
            "(4) Service account and API key management procedures."
        ),
        'technical': (
            "Provide: (1) IAM credential report showing MFA status for all users, "
            "(2) IAM Identity Center (SSO) configuration with identity provider federation, "
            "(3) IAM password policy configuration screenshot, "
            "(4) AWS Config compliance reports for IAM credential rules "
            "(IAM_USER_MFA_ENABLED, ACCESS_KEYS_ROTATED, IAM_USER_UNUSED_CREDENTIALS_CHECK), "
            "(5) Secrets Manager rotation configuration for service credentials."
        ),
        'keywords': {
            'federation': (
                "Provide: (1) SAML/OIDC federation configuration between IdP and AWS, "
                "(2) IAM Identity Center identity source configuration, "
                "(3) Certificate management records for federation trust, "
                "(4) Token/assertion security settings (signing, encryption, expiration)."
            ),
        },
    },
    'IR': {
        'policy': (
            "Provide: (1) Incident response policy and plan document with version history, "
            "(2) Incident severity classification criteria, "
            "(3) Escalation procedures and contact lists, "
            "(4) Third-party coordination procedures (AWS Support, law enforcement, regulators)."
        ),
        'technical': (
            "Provide: (1) AWS-specific incident response runbooks (compromised credentials, S3 exposure, unauthorized EC2), "
            "(2) GuardDuty and Security Hub automated response configurations (EventBridge rules, Lambda functions), "
            "(3) Incident response exercise records (tabletop exercises, simulations), "
            "(4) Post-incident review reports with lessons learned, "
            "(5) Evidence collection procedures (EBS snapshots, CloudTrail exports, memory capture)."
        ),
        'keywords': {
            'detection': (
                "Provide: (1) GuardDuty finding type coverage and notification configurations, "
                "(2) Security Hub integration sources and automated finding aggregation, "
                "(3) SIEM correlation rules for AWS event sources."
            ),
            'containment': (
                "Provide: (1) Containment runbooks (security group isolation, IAM key disabling, WAF blocking), "
                "(2) Automated containment Lambda functions or Security Hub custom actions, "
                "(3) Containment action records from recent incidents with timestamps."
            ),
        },
    },
    'MA': {
        'policy': (
            "Provide: (1) System maintenance policy document with approval records, "
            "(2) Maintenance scheduling and authorization procedures, "
            "(3) Remote maintenance access controls and monitoring requirements, "
            "(4) Maintenance personnel authorization records."
        ),
        'technical': (
            "Provide: (1) Systems Manager Patch Manager compliance reports showing patch status across EC2 fleet, "
            "(2) Systems Manager Maintenance Window configurations and execution history, "
            "(3) Amazon Inspector vulnerability findings showing patching gaps, "
            "(4) CloudTrail logs of maintenance-related API calls (instance stop/start, AMI creation)."
        ),
        'keywords': {},
    },
    'MP': {
        'policy': (
            "Provide: (1) Media protection policy covering data-at-rest encryption requirements, "
            "(2) Media sanitization and disposal procedures, "
            "(3) Data transport and handling procedures for AWS environments, "
            "(4) Policy review and approval records."
        ),
        'technical': (
            "Provide: (1) AWS Config compliance reports for encryption rules "
            "(ENCRYPTED_VOLUMES, S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED, RDS_STORAGE_ENCRYPTED), "
            "(2) KMS key policies and rotation configurations, "
            "(3) S3 bucket policies enforcing encryption, "
            "(4) EBS default encryption configuration evidence per Region."
        ),
        'keywords': {},
    },
    'PE': {
        'policy': (
            "Provide: (1) Physical and environmental protection policy document, "
            "(2) AWS Artifact SOC reports documenting AWS data center physical controls, "
            "(3) For on-premises infrastructure: physical access control procedures, "
            "(4) Shared responsibility model documentation for physical security."
        ),
        'technical': (
            "Provide: (1) AWS Artifact SOC 2 Type II report sections covering physical security, "
            "(2) For hybrid/on-premises: physical access logs, surveillance records, visitor logs, "
            "(3) Direct Connect facility physical security documentation, "
            "(4) Remote work endpoint security compliance evidence."
        ),
        'keywords': {},
    },
    'PL': {
        'policy': (
            "Provide: (1) System security plan (SSP) document for AWS workloads, "
            "(2) Rules of behavior for AWS users, "
            "(3) Security architecture documentation showing AWS service integration, "
            "(4) Plan review and update records."
        ),
        'technical': (
            "Provide: (1) AWS architecture diagrams showing security controls placement, "
            "(2) Security plan mapping to AWS shared responsibility model, "
            "(3) Rules of behavior acknowledgment records, "
            "(4) Architecture review records showing security considerations."
        ),
        'keywords': {},
    },
    'PM': {
        'policy': (
            "Provide: (1) Information security program plan document, "
            "(2) Risk management strategy documentation, "
            "(3) Security program governance structure and roles, "
            "(4) Program review and update records."
        ),
        'technical': (
            "Provide: (1) Security Hub aggregated compliance scores across accounts, "
            "(2) AWS Organizations structure showing security governance, "
            "(3) Security program metrics dashboard or reports, "
            "(4) Risk register with AWS-specific entries and treatment plans."
        ),
        'keywords': {},
    },
    'PS': {
        'policy': (
            "Provide: (1) Personnel security policy covering screening, transfer, and termination, "
            "(2) Access agreement templates and signed records, "
            "(3) Personnel screening procedures for AWS-privileged roles, "
            "(4) Policy review and approval records."
        ),
        'technical': (
            "Provide: (1) IAM user deprovisioning records correlated with HR termination dates, "
            "(2) Access key deletion records for terminated personnel, "
            "(3) IAM credential report showing no active credentials for former employees, "
            "(4) Access agreement acknowledgment records for current personnel."
        ),
        'keywords': {},
    },
    'PT': {
        'policy': (
            "Provide: (1) PII processing and transparency policy document, "
            "(2) Privacy impact assessment (PIA) records for AWS workloads, "
            "(3) Data subject rights procedures documentation, "
            "(4) Privacy notice and consent management documentation."
        ),
        'technical': (
            "Provide: (1) Amazon Macie sensitive data discovery reports for S3, "
            "(2) Data classification tagging evidence from AWS Config, "
            "(3) S3 access logging and CloudTrail data event configurations for PII stores, "
            "(4) Encryption configurations for PII data stores (RDS, DynamoDB, S3)."
        ),
        'keywords': {},
    },
    'RA': {
        'policy': (
            "Provide: (1) Risk assessment policy and methodology document, "
            "(2) Risk assessment schedule and scope definitions, "
            "(3) Risk tolerance and acceptance criteria documentation, "
            "(4) Policy review and approval records."
        ),
        'technical': (
            "Provide: (1) Amazon Inspector vulnerability scan reports for EC2 and container workloads, "
            "(2) Security Hub findings summary showing risk posture, "
            "(3) AWS Config non-compliant resource reports, "
            "(4) Risk register with AWS-specific entries, likelihood, impact, and treatment plans, "
            "(5) Vulnerability remediation tracking records with SLA compliance."
        ),
        'keywords': {
            'vulnerability': (
                "Provide: (1) Amazon Inspector continuous scanning configuration and findings, "
                "(2) ECR image scan results for container vulnerabilities, "
                "(3) Vulnerability remediation SLA documentation and compliance metrics, "
                "(4) Patch management reports from Systems Manager."
            ),
        },
    },
    'SA': {
        'policy': (
            "Provide: (1) System and services acquisition policy document, "
            "(2) Secure development lifecycle (SDLC) procedures, "
            "(3) Supply chain risk management procedures, "
            "(4) Third-party service assessment requirements."
        ),
        'technical': (
            "Provide: (1) CI/CD pipeline configuration showing security scanning stages (SAST, DAST, SCA), "
            "(2) CodeGuru or third-party code review tool reports, "
            "(3) Dependency vulnerability scan results from build pipeline, "
            "(4) Third-party service compliance documentation (SOC 2, ISO 27001 reports), "
            "(5) AWS Marketplace subscription security assessments."
        ),
        'keywords': {
            'development': (
                "Provide: (1) Secure SDLC policy and procedures, "
                "(2) Code review records and security scan results, "
                "(3) Developer security training completion records, "
                "(4) Security testing results (SAST, DAST, penetration testing)."
            ),
            'supply_chain': (
                "Provide: (1) Supplier risk assessment records, "
                "(2) Third-party compliance certification reviews, "
                "(3) Software composition analysis (SCA) reports, "
                "(4) SBOM documentation for critical applications."
            ),
        },
    },
    'SC': {
        'policy': (
            "Provide: (1) System and communications protection policy document, "
            "(2) Encryption standards and requirements documentation, "
            "(3) Network segmentation and boundary protection requirements, "
            "(4) Policy review and approval records."
        ),
        'technical': (
            "Provide: (1) Security group configurations showing least-privilege network rules, "
            "(2) Network ACL configurations for VPC subnets, "
            "(3) ACM certificate inventory showing TLS in use for data in transit, "
            "(4) AWS Config compliance reports for encryption and network rules "
            "(VPC_DEFAULT_SECURITY_GROUP_CLOSED, RESTRICTED_INCOMING_TRAFFIC, S3_BUCKET_SSL_REQUESTS_ONLY), "
            "(5) WAF rule configurations for web application protection."
        ),
        'keywords': {
            'encryption': (
                "Provide: (1) KMS key inventory with key policies and rotation status, "
                "(2) AWS Config reports for encryption rules across services, "
                "(3) ACM certificate configurations for TLS, "
                "(4) S3 bucket policies requiring encryption and secure transport."
            ),
            'boundary': (
                "Provide: (1) VPC architecture diagrams showing network segmentation, "
                "(2) AWS Network Firewall or third-party firewall configurations, "
                "(3) VPC endpoint configurations for private AWS service access, "
                "(4) Transit Gateway route table configurations."
            ),
        },
    },
    'SI': {
        'policy': (
            "Provide: (1) System and information integrity policy document, "
            "(2) Flaw remediation procedures and SLA requirements, "
            "(3) Malicious code protection requirements, "
            "(4) Security monitoring requirements and procedures."
        ),
        'technical': (
            "Provide: (1) GuardDuty findings summary and response records, "
            "(2) Amazon Inspector vulnerability findings and remediation status, "
            "(3) Systems Manager Patch Manager compliance reports, "
            "(4) Security Hub findings trend reports showing remediation progress, "
            "(5) CloudWatch alarms for security-relevant system events."
        ),
        'keywords': {
            'monitoring': (
                "Provide: (1) GuardDuty detector configuration across all accounts and Regions, "
                "(2) Security Hub enabled standards and integration sources, "
                "(3) CloudWatch alarm configurations for security events, "
                "(4) SIEM integration evidence showing AWS log source ingestion."
            ),
            'flaw': (
                "Provide: (1) Vulnerability remediation tracking records with SLA metrics, "
                "(2) Systems Manager Patch Manager compliance reports, "
                "(3) Amazon Inspector scan frequency and coverage evidence, "
                "(4) Emergency patching procedure documentation and execution records."
            ),
        },
    },
    'SR': {
        'policy': (
            "Provide: (1) Supply chain risk management policy document, "
            "(2) Supplier assessment and monitoring procedures, "
            "(3) Acquisition security requirements documentation, "
            "(4) Policy review and approval records."
        ),
        'technical': (
            "Provide: (1) Third-party service inventory with risk classifications, "
            "(2) Supplier compliance certification records (SOC 2, ISO 27001), "
            "(3) Software composition analysis (SCA) reports for third-party dependencies, "
            "(4) AWS Marketplace subscription security review records, "
            "(5) SBOM documentation for critical applications."
        ),
        'keywords': {},
    },
}


def get_family_evidence_question(control_id: str, control_title: str = '') -> Optional[str]:
    """Get a family-level evidence question for a NIST 800-53 control.

    Selects the appropriate evidence template based on the control family
    and whether the control is a policy control (-1 suffix) or technical.
    Also checks for keyword matches in the control title to provide more
    specific evidence guidance.

    Args:
        control_id: Control ID (e.g., 'AC-2', 'AU-6')
        control_title: Optional control title for keyword matching

    Returns:
        Evidence question string, or None if family not found
    """
    parts = control_id.upper().split('-')
    if len(parts) < 2:
        return None

    family = parts[0]
    control_num = parts[1] if len(parts) > 1 else ''

    template = FAMILY_EVIDENCE_TEMPLATES.get(family)
    if not template:
        return None

    # Check for keyword-specific evidence first
    if control_title and template.get('keywords'):
        title_lower = control_title.lower()
        for keyword, question in template['keywords'].items():
            if keyword in title_lower:
                return f"What evidence demonstrates {control_id} compliance? {question}"

    # Policy controls (-1 suffix)
    is_policy = control_num == '1' or control_num == '01'
    if is_policy:
        return f"What evidence demonstrates {control_id} compliance? {template['policy']}"

    # Technical controls
    return f"What evidence demonstrates {control_id} compliance? {template['technical']}"


def has_family_evidence_question(control_id: str) -> bool:
    """Check if a family-level evidence template exists for this control."""
    parts = control_id.upper().split('-')
    if len(parts) < 2:
        return False
    return parts[0] in FAMILY_EVIDENCE_TEMPLATES

"""AWS Shared Responsibility Model mappings for NIST CSF 2.0 subcategories.

Maps CSF subcategories to aws/shared/customer responsibility based on the
AWS Shared Responsibility Model.

RESPONSIBILITY CATEGORIES:
- AWS: Controls AWS implements for infrastructure (physical, hardware, network)
- Shared: AWS provides tools/services, customers must configure and use them
- Customer: Customers implement entirely (governance, policy, procedures)
"""

from typing import Dict, List

# CSF subcategories where AWS is primarily responsible (cloud-hosted workloads)
# Customer evidence: AWS SOC 2/ISO 27001 reports via AWS Artifact
AWS_RESPONSIBILITY_SUBCATEGORIES = [
    # Physical environment monitoring (AWS data centers)
    'de.cm-02',
    # Physical access management (AWS facilities)
    'pr.aa-06',
    # Environmental threat protection (AWS data centers - power, cooling, fire, flood)
    'pr.ir-02',
    # Hardware maintenance/replacement (AWS manages underlying infrastructure)
    'pr.ps-03',
]

# CSF subcategories with shared responsibility and relevant AWS services
AWS_MANAGED_SUBCATEGORIES: Dict[str, List[str]] = {
    # === IDENTIFY (ID) ===
    'id.am-01': ['AWS Config', 'Systems Manager Inventory', 'Resource Groups'],
    'id.am-02': ['AWS Config', 'Systems Manager', 'License Manager'],
    'id.am-03': ['VPC Flow Logs', 'Network Manager', 'Transit Gateway'],
    'id.am-04': ['AWS Marketplace', 'Service Catalog'],
    'id.am-05': ['AWS Config', 'Resource Groups', 'Tag Editor'],
    'id.am-07': ['Macie', 'Lake Formation', 'Glue Data Catalog'],
    'id.am-08': ['AWS Config', 'Systems Manager', 'EC2 Image Builder'],
    'id.ra-01': ['Inspector', 'Security Hub', 'GuardDuty'],
    'id.ra-02': ['GuardDuty', 'Security Hub'],
    'id.ra-03': ['GuardDuty', 'Security Hub', 'Detective'],
    'id.ra-04': ['Inspector', 'Security Hub'],
    'id.ra-05': ['Security Hub', 'Inspector', 'GuardDuty'],
    'id.ra-07': ['AWS Config', 'CloudTrail', 'Service Catalog'],
    'id.ra-08': ['Inspector', 'Security Hub'],
    'id.ra-09': ['Inspector', 'ECR Image Scanning', 'Signer'],  # HW/SW authenticity
    'id.im-01': ['Security Hub', 'AWS Config', 'Trusted Advisor'],
    'id.im-02': ['Inspector', 'GuardDuty', 'Security Hub'],
    'id.im-03': ['CloudWatch', 'AWS Config', 'Trusted Advisor'],  # Operational improvements
    'id.im-04': ['Systems Manager Incident Manager', 'Lambda', 'Step Functions'],  # IR plan testing

    # === PROTECT (PR) ===
    'pr.aa-01': ['IAM', 'IAM Identity Center', 'Organizations'],
    'pr.aa-02': ['IAM', 'Cognito', 'IAM Identity Center'],
    'pr.aa-03': ['IAM MFA', 'Cognito', 'IAM Identity Center'],
    'pr.aa-04': ['IAM', 'STS', 'Cognito'],
    'pr.aa-05': ['IAM Policies', 'Organizations SCPs', 'IAM Access Analyzer'],
    'pr.ds-01': ['KMS', 'S3 Encryption', 'EBS Encryption', 'RDS Encryption'],
    'pr.ds-02': ['ACM', 'CloudFront', 'ELB TLS', 'VPN'],
    'pr.ds-10': ['Nitro Enclaves', 'KMS', 'CloudHSM'],
    'pr.ds-11': ['AWS Backup', 'S3 Versioning', 'RDS Snapshots', 'EBS Snapshots'],
    'pr.ps-01': ['AWS Config', 'Systems Manager', 'CloudFormation'],
    'pr.ps-02': ['Systems Manager Patch Manager', 'Inspector'],
    'pr.ps-04': ['CloudTrail', 'CloudWatch Logs', 'VPC Flow Logs'],
    'pr.ps-05': ['Systems Manager', 'AppStream', 'WorkSpaces'],
    'pr.ps-06': ['CodeGuru', 'CodePipeline', 'CodeBuild'],
    'pr.ir-01': ['Security Groups', 'NACLs', 'WAF', 'Shield', 'Network Firewall'],
    'pr.ir-03': ['Auto Scaling', 'Multi-AZ', 'Route 53', 'Elastic Disaster Recovery'],
    'pr.ir-04': ['Auto Scaling', 'CloudWatch', 'Trusted Advisor'],

    # === DETECT (DE) ===
    'de.cm-01': ['VPC Flow Logs', 'GuardDuty', 'Network Firewall', 'CloudWatch'],
    'de.cm-03': ['CloudTrail', 'IAM Access Analyzer', 'GuardDuty'],
    'de.cm-06': ['GuardDuty', 'Security Hub', 'CloudTrail'],
    'de.cm-09': ['GuardDuty', 'Inspector', 'Macie', 'CloudWatch'],
    'de.ae-02': ['Detective', 'Security Hub', 'CloudWatch Logs Insights'],
    'de.ae-03': ['Security Hub', 'Detective', 'CloudWatch'],
    'de.ae-04': ['Security Hub', 'Detective', 'GuardDuty'],
    'de.ae-06': ['Security Hub', 'SNS', 'EventBridge'],
    'de.ae-07': ['GuardDuty', 'Security Hub', 'Detective'],

    # === RESPOND (RS) ===
    'rs.an-03': ['Detective', 'CloudTrail', 'Athena'],
    'rs.an-06': ['CloudTrail', 'S3 Object Lock', 'CloudWatch Logs'],
    'rs.an-07': ['CloudTrail', 'S3', 'CloudWatch Logs'],
    'rs.an-08': ['Detective', 'GuardDuty', 'Security Hub'],  # Incident magnitude estimation
    'rs.mi-01': ['Security Groups', 'WAF', 'Network Firewall', 'Lambda'],
    'rs.mi-02': ['Systems Manager', 'Lambda', 'Step Functions'],
    'rs.ma-01': ['Systems Manager Incident Manager', 'AWS Support', 'EventBridge'],  # IR coordination

    # === RECOVER (RC) ===
    'rc.rp-01': ['AWS Backup', 'Elastic Disaster Recovery', 'Systems Manager Incident Manager'],  # Recovery execution
    'rc.rp-02': ['AWS Backup', 'Elastic Disaster Recovery', 'CloudFormation'],
    'rc.rp-03': ['AWS Backup', 'S3 Object Lock'],
    'rc.rp-04': ['Route 53', 'CloudFront', 'Elastic Disaster Recovery'],  # Mission function continuity
    'rc.rp-05': ['CloudFormation', 'Elastic Disaster Recovery', 'AWS Backup'],
}

# Customer-only subcategories (governance, policy, organizational processes)
# These are implicitly anything not in AWS_RESPONSIBILITY or AWS_MANAGED


def get_csf_responsibility(subcategory_id: str) -> str:
    """Determine AWS shared responsibility for a CSF subcategory.

    Args:
        subcategory_id: CSF subcategory ID (e.g., "GV.OC-01" or "PR.DS-01")

    Returns:
        'aws', 'shared', or 'customer'
    """
    normalized = subcategory_id.lower()

    if normalized in AWS_RESPONSIBILITY_SUBCATEGORIES:
        return 'aws'
    elif normalized in AWS_MANAGED_SUBCATEGORIES:
        return 'shared'
    else:
        return 'customer'


def get_csf_aws_services(subcategory_id: str) -> List[str]:
    """Get AWS services relevant to a CSF subcategory.

    Args:
        subcategory_id: CSF subcategory ID

    Returns:
        List of AWS service names
    """
    return AWS_MANAGED_SUBCATEGORIES.get(subcategory_id.lower(), [])
